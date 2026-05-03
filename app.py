from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import session
from config import Config
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ================= MODEL =================

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    cabang = db.Column(db.String(100))

class Material(db.Model):
    __tablename__ = "material"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    harga = db.Column(db.BigInteger)

class KirimStok(db.Model):
    __tablename__ = "kirim_stok"
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer)
    cabang = db.Column(db.String(100))
    jumlah_truck = db.Column(db.Integer)
    total_kubik = db.Column(db.Float)
    status = db.Column(db.String(50))
    tanggal = db.Column(db.Date, default=datetime.today)


class StokCabang(db.Model):
    __tablename__ = "stok_cabang"
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer)
    lokasi = db.Column(db.String(100))
    total_kubik = db.Column(db.Float, default=0)
    
class Keuangan(db.Model):
    __tablename__ = "keuangan"

    id = db.Column(db.Integer, primary_key=True)
    tipe = db.Column(db.String(20))  # pemasukan / pengeluaran
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=True)
    cabang = db.Column(db.String(100))
    jenis_truck = db.Column(db.String(100), nullable=True)
    kubikasi = db.Column(db.Float, nullable=True)
    jumlah = db.Column(db.BigInteger)
    keterangan = db.Column(db.String(200), nullable=True)
    metode = db.Column(db.String(50), nullable=True)
    tanggal = db.Column(db.Date)
    status = db.Column(db.String(20), default="Draft")

    material = db.relationship("Material")
# ================= LOGIN =================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Login gagal")
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# ================= DASHBOARD =================
from calendar import monthrange
import calendar

@app.route('/dashboard')
@login_required
def dashboard():

    # ================= DASHBOARD ADMIN =================
    if current_user.role == "admin":

        now = datetime.now()

        cabang_filter = request.args.get("cabang")
        bulan_input = request.args.get("bulan")

        if bulan_input:
            tahun = int(bulan_input.split("-")[0])
            bulan = int(bulan_input.split("-")[1])
        else:
            tahun = now.year
            bulan = now.month

        query = Keuangan.query.filter(
            db.extract('year', Keuangan.tanggal) == tahun,
            Keuangan.status == "Final"
        )

        if cabang_filter:
            query = query.filter(Keuangan.cabang == cabang_filter)

        data_bulan_ini = query.filter(
            db.extract('month', Keuangan.tanggal) == bulan
        ).all()

        total_pemasukan = sum(d.jumlah for d in data_bulan_ini if d.tipe == "pemasukan")
        total_pengeluaran = sum(d.jumlah for d in data_bulan_ini if d.tipe == "pengeluaran")

        total_laporan = len(
            set((d.cabang, d.tanggal) for d in data_bulan_ini)
        )

        jumlah_hari = monthrange(tahun, bulan)[1]

        pemasukan_per_bulan = []
        pengeluaran_per_bulan = []
        label_bulan = []

        for hari in range(1, jumlah_hari + 1):

            data_harian = query.filter(
                db.extract('month', Keuangan.tanggal) == bulan,
                db.extract('day', Keuangan.tanggal) == hari
            ).all()

            pemasukan_per_bulan.append(
                sum(d.jumlah for d in data_harian if d.tipe == "pemasukan")
            )

            pengeluaran_per_bulan.append(
                sum(d.jumlah for d in data_harian if d.tipe == "pengeluaran")
            )

            label_bulan.append(str(hari))

        nama_bulan = calendar.month_name[bulan]
        materials = Material.query.all()
        # ================= RANKING CABANG =================
        ranking_data = db.session.query(
            Keuangan.cabang,
            db.func.sum(Keuangan.jumlah).label('total')
        ).filter(
            Keuangan.tipe == "pemasukan",
            Keuangan.status == "Final",
            db.extract('year', Keuangan.tanggal) == tahun,
            db.extract('month', Keuangan.tanggal) == bulan
        ).group_by(Keuangan.cabang).order_by(db.desc('total')).all()
        # ================= DISTRIBUSI CABANG =================
        cabang_labels = []
        cabang_totals = []

        for r in ranking_data:
            cabang_labels.append(r.cabang)
            cabang_totals.append(r.total)

        # ================= STOK MENIPIS SEMUA CABANG =================
        stok_menipis_all = db.session.query(
            StokCabang,
            Material.nama
        ).join(
            Material, Material.id == StokCabang.material_id
        ).filter(
            StokCabang.total_kubik < 30,
            StokCabang.lokasi != "Pusat"
        ).all()

        return render_template(
            "dashboard_admin.html",
            total_pemasukan=total_pemasukan,
            total_pengeluaran=total_pengeluaran,
            total_laporan=total_laporan,
            bulan=bulan,
            tahun=tahun,
            nama_bulan=nama_bulan,
            bulan_input=f"{tahun}-{str(bulan).zfill(2)}",
            pemasukan_per_bulan=pemasukan_per_bulan,
            pengeluaran_per_bulan=pengeluaran_per_bulan,
            label_bulan=label_bulan,
            ranking_data=ranking_data,
            cabang_labels=cabang_labels,
            cabang_totals=cabang_totals,
            materials=materials,
            stok_menipis_all=stok_menipis_all,
            cabang_filter=cabang_filter
        )

    # ================= DASHBOARD CABANG =================

    today = datetime.today().date()

    tanggal_hari_ini = today.strftime("%d %B %Y")
    today_link = today.strftime("%Y-%m-%d")

    transaksi_hari_ini = Keuangan.query.filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == today,
        Keuangan.tipe == "pemasukan"
    ).count()

    pengeluaran_hari_ini = Keuangan.query.filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == today,
        Keuangan.tipe == "pengeluaran"
    ).count()

    total_pemasukan_hari_ini = db.session.query(
        db.func.sum(Keuangan.jumlah)
    ).filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == today,
        Keuangan.tipe == "pemasukan"
    ).scalar() or 0

    total_pengeluaran_hari_ini = db.session.query(
        db.func.sum(Keuangan.jumlah)
    ).filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == today,
        Keuangan.tipe == "pengeluaran"
    ).scalar() or 0
    # ================= STOK MENIPIS CABANG =================
    stok_menipis = db.session.query(
        StokCabang,
        Material.nama
    ).join(
        Material, Material.id == StokCabang.material_id
    ).filter(
        StokCabang.lokasi == current_user.cabang,
        StokCabang.total_kubik < 30
    ).all()
    return render_template(
        "dashboard_cabang.html",
        tanggal_hari_ini=tanggal_hari_ini,
        transaksi_hari_ini=transaksi_hari_ini,
        pengeluaran_hari_ini=pengeluaran_hari_ini,
        laporan_hari_ini=1,
        total_pemasukan_hari_ini=total_pemasukan_hari_ini,
        total_pengeluaran_hari_ini=total_pengeluaran_hari_ini,
        stok_menipis=stok_menipis,
        today=today_link
    )
# ================= USER =================

@app.route('/user', methods=['GET','POST'])
@login_required
def user():
    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        u = User(
            username=request.form['username'],
            password=request.form['password'],
            role=request.form['role'],
            cabang=request.form['cabang']
        )
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('user'))

    return render_template("user.html", data=User.query.all())
# ================= EDIT USER =================
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.role = request.form['role']
        user.cabang = request.form['cabang']

        db.session.commit()
        flash("User berhasil diperbarui", "success")
        return redirect(url_for('user'))

    return render_template("edit_user.html", user=user)
# ================= HAPUS USER =================
@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(id)

    # 🔥 Proteksi: admin tidak bisa hapus dirinya sendiri
    if user.id == current_user.id:
        flash("Anda tidak bisa menghapus akun sendiri", "danger")
        return redirect(url_for('user'))

    db.session.delete(user)
    db.session.commit()

    flash("User berhasil dihapus", "success")
    return redirect(url_for('user'))
# ================= MATERIAL =================

@app.route('/material', methods=['GET','POST'])
@login_required
def material():
    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        m = Material(
            nama=request.form['nama'],
            harga=request.form['harga']
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('material'))

    return render_template("material.html", data=Material.query.all())
# ================= EDIT MATERIAL =================
@app.route('/edit_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_material(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    material = Material.query.get_or_404(id)

    if request.method == 'POST':
        material.nama = request.form['nama']
        material.harga = request.form['harga']

        db.session.commit()
        flash("Material berhasil diperbarui", "success")
        return redirect(url_for('material'))

    return render_template("edit_material.html", material=material)
# ================= HAPUS MATERIAL =================
@app.route('/delete_material/<int:id>')
@login_required
def delete_material(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    material = Material.query.get_or_404(id)

    db.session.delete(material)
    db.session.commit()

    flash("Material berhasil dihapus", "success")
    return redirect(url_for('material'))

# ================= KIRIM STOK =================
@app.route('/kirim', methods=['GET','POST'])
@login_required
def kirim():
    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    # ================= POST =================
    if request.method == 'POST':

        material_id = int(request.form['material'])
        cabang = request.form['cabang']
        jumlah_truck = int(request.form['jumlah_truck'])
        total_kubik = float(request.form['total_kubik'])

        # ================= CEK STOK PUSAT =================
        stok_pusat = StokCabang.query.filter_by(
            material_id=material_id,
            lokasi="Pusat"
        ).first()

        if not stok_pusat:
            flash("Stok pusat untuk material ini belum tersedia", "danger")
            return redirect(url_for('kirim'))

        if stok_pusat.total_kubik < total_kubik:
            flash("Stok pusat tidak mencukupi untuk pengiriman ini", "danger")
            return redirect(url_for('kirim'))

        # ================= SIMPAN DATA PENGIRIMAN =================
        kirim = KirimStok(
            material_id=material_id,
            cabang=cabang,
            jumlah_truck=jumlah_truck,
            total_kubik=total_kubik,
            status="Menunggu",
            tanggal=datetime.today()
        )

        db.session.add(kirim)
        db.session.commit()

        flash("Stok berhasil dikirim", "success")
        return redirect(url_for('kirim'))

    # ================= FILTER TANGGAL =================
    tanggal_filter = request.args.get("tanggal")

    query = KirimStok.query

    if tanggal_filter:
        try:
            tanggal_obj = datetime.strptime(tanggal_filter, "%Y-%m-%d").date()
            query = query.filter(KirimStok.tanggal == tanggal_obj)
        except:
            flash("Format tanggal salah")

    # ================= ORDER & PAGINATION =================
    page = request.args.get('page', 1, type=int)

    pagination = query.order_by(KirimStok.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    data = pagination.items

    return render_template(
        "kirim_stok.html",
        materials=Material.query.all(),
        data=data,
        pagination=pagination,
        tanggal_filter=tanggal_filter,
        today=datetime.today().strftime("%Y-%m-%d")
    )
# ================= EDIT KIRIM STOK =================
@app.route('/edit_kirim/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_kirim(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    kirim = KirimStok.query.get_or_404(id)

    # 🔥 Tidak boleh edit jika sudah dikonfirmasi
    if kirim.status == "Dikonfirmasi":
        flash("Pengiriman sudah dikonfirmasi dan tidak bisa diubah", "danger")
        return redirect(url_for('kirim'))

    if request.method == 'POST':
        kirim.material_id = request.form['material']
        kirim.cabang = request.form['cabang']
        kirim.jumlah_truck = request.form['jumlah_truck']
        kirim.total_kubik = request.form['total_kubik']

        db.session.commit()
        flash("Data pengiriman berhasil diperbarui", "success")
        return redirect(url_for('kirim'))

    return render_template("edit_kirim.html",
                           kirim=kirim,
                           materials=Material.query.all())
# ================= HAPUS KIRIM STOK =================
@app.route('/delete_kirim/<int:id>')
@login_required
def delete_kirim(id):

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    kirim = KirimStok.query.get_or_404(id)

    # 🔥 Tidak boleh hapus jika sudah dikonfirmasi
    if kirim.status == "Dikonfirmasi":
        flash("Pengiriman sudah dikonfirmasi dan tidak bisa dihapus", "danger")
        return redirect(url_for('kirim'))

    db.session.delete(kirim)
    db.session.commit()

    flash("Pengiriman berhasil dihapus", "success")
    return redirect(url_for('kirim'))
# ================= MONITOR STOK =================
@app.route('/monitor_stok')
@login_required
def monitor_stok():

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    cabang = request.args.get('cabang')
    data = []

    if cabang:
        data = StokCabang.query.filter_by(lokasi=cabang).all()

    return render_template(
        "monitor_stok.html",
        materials=Material.query.all(),
        data=data,
        cabang=cabang
    )
# ================= STOK CABANG =================
@app.route('/stok_cabang')
@login_required
def stok_cabang():

    if current_user.role != "cabang":
        return redirect(url_for('dashboard'))

    data = StokCabang.query.filter_by(
        lokasi=current_user.cabang
    ).all()

    return render_template(
        'stok_cabang.html',
        data=data,
        materials=Material.query.all(),
        cabang=current_user.cabang
    )

# ================= KONFIRMASI STOK =================

@app.route('/konfirmasi_stok')
@login_required
def konfirmasi_stok():
    if current_user.role != "cabang":
        return redirect(url_for('dashboard'))

    data = KirimStok.query.filter_by(
        cabang=current_user.cabang,
        status="Menunggu"
    ).all()

    return render_template("konfirmasi_stok.html",
                           data=data,
                           materials=Material.query.all())

@app.route('/proses_konfirmasi/<int:id>')
@login_required
def proses_konfirmasi(id):

    kirim = KirimStok.query.get(id)

    if kirim and kirim.cabang == current_user.cabang:

        # ================= STOK CABANG =================
        stok_cabang = StokCabang.query.filter_by(
            material_id=kirim.material_id,
            lokasi=current_user.cabang
        ).first()

        if stok_cabang:
            stok_cabang.total_kubik = round(
                stok_cabang.total_kubik + kirim.total_kubik, 2
            )
        else:
            stok_cabang = StokCabang(
                material_id=kirim.material_id,
                lokasi=current_user.cabang,
                total_kubik=round(kirim.total_kubik, 2)
            )
            db.session.add(stok_cabang)

        # ================= STOK PUSAT =================
        stok_pusat = StokCabang.query.filter_by(
            material_id=kirim.material_id,
            lokasi="Pusat"
        ).first()

        if not stok_pusat:
            flash("Stok pusat belum tersedia", "danger")
            return redirect(url_for('konfirmasi_stok'))

        # cek stok pusat cukup
        if stok_pusat.total_kubik < kirim.total_kubik:
            flash("Stok pusat tidak mencukupi", "danger")
            return redirect(url_for('konfirmasi_stok'))

        # kurangi stok pusat
        stok_pusat.total_kubik = round(
            stok_pusat.total_kubik - kirim.total_kubik, 2
        )

        # ================= UPDATE STATUS =================
        kirim.status = "Dikonfirmasi"

        db.session.commit()

        flash("Stok berhasil dikonfirmasi", "success")

    return redirect(url_for('konfirmasi_stok'))

# ================= LAPORAN CABANG =================
@app.route('/laporan_cabang', methods=['GET','POST'])
@login_required
def laporan_cabang():

    if current_user.role != "cabang":
        return redirect(url_for('dashboard'))

    tanggal = request.args.get('tanggal')

    # jika user klik menu laporan tanpa tanggal → reset session
    if not tanggal:
        session.pop("laporan_tanggal", None)
        session.pop("edit_mode", None)

        today = datetime.today().strftime("%Y-%m-%d")

        return render_template(
            "pilih_tanggal.html",
            cabang=current_user.cabang,
            today=today
        )
    session["laporan_tanggal"] = tanggal
    tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")

    # ================= PROSES KONFIRMASI YES =================
    if request.args.get("confirm") == "yes":

        session["edit_mode"] = True

        Keuangan.query.filter_by(
            cabang=current_user.cabang,
            tanggal=tanggal_obj
        ).update({"status": "Draft"})

        db.session.commit()

        return redirect(url_for('laporan_cabang', tanggal=tanggal))
    # ================= CEK DATA FINAL =================
    data_final = Keuangan.query.filter_by(
        cabang=current_user.cabang,
        tanggal=tanggal_obj,
        status="Final"
    ).first()

    # ================= POPUP KONFIRMASI EDIT =================
    if data_final and not session.get("edit_mode"):
        return render_template(
            "konfirmasi_edit.html",
            tanggal=tanggal
        )

    # ================= INPUT DATA =================
    if request.method == 'POST':

        # ================= PEMASUKAN =================
        if 'material' in request.form:

            material = Material.query.get(int(request.form['material']))
            jenis_truck = request.form.get('jenis_truck')
            kubikasi_input = request.form.get('kubikasi')

            if not kubikasi_input:
                flash("Kubikasi wajib diisi", "warning")
                return redirect(url_for('laporan_cabang', tanggal=tanggal))

            kubikasi = float(kubikasi_input)

            stok = StokCabang.query.filter_by(
                material_id=material.id,
                lokasi=current_user.cabang
            ).first()

            if not stok:
                flash("Stok tidak tersedia", "danger")
                return redirect(url_for('laporan_cabang', tanggal=tanggal))

            if stok.total_kubik < kubikasi:
                flash("Kubikasi melebihi stok tersedia", "danger")
                return redirect(url_for('laporan_cabang', tanggal=tanggal))

            harga_per_m3 = material.harga / 4.5
            total = round(kubikasi * harga_per_m3)
            total = round(total / 1000) * 1000

            stok.total_kubik = round(stok.total_kubik - kubikasi, 2)

            pemasukan = Keuangan(
                tipe="pemasukan",
                material_id=material.id,
                cabang=current_user.cabang,
                jenis_truck=jenis_truck,
                kubikasi=kubikasi,
                jumlah=int(total),
                metode=request.form.get('metode'),
                tanggal=tanggal_obj,
                status="Draft"
            )

            db.session.add(pemasukan)
            db.session.commit()

        # ================= PENGELUARAN =================
        elif 'keterangan' in request.form:

            jumlah_input = request.form.get('jumlah')

            if not jumlah_input:
                flash("Jumlah wajib diisi")
                return redirect(url_for('laporan_cabang', tanggal=tanggal))

            pengeluaran = Keuangan(
                tipe="pengeluaran",
                cabang=current_user.cabang,
                keterangan=request.form['keterangan'],
                jumlah=float(jumlah_input),
                tanggal=tanggal_obj,
                status="Draft"
            )

            db.session.add(pengeluaran)
            db.session.commit()

        return redirect(url_for('laporan_cabang', tanggal=tanggal))

    # ================= AMBIL DATA =================

    page_transaksi = request.args.get('page_transaksi', 1, type=int)

    pemasukan_pagination = Keuangan.query.filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pemasukan",
        Keuangan.status.in_(["Draft","Final"])
    ).order_by(Keuangan.id.desc()).paginate(
        page=page_transaksi,
        per_page=10,
        error_out=False
    )

    pemasukan = pemasukan_pagination.items

    pengeluaran = Keuangan.query.filter(
        Keuangan.cabang == current_user.cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pengeluaran",
        Keuangan.status.in_(["Draft","Final"])
    ).all()

    total_pemasukan = sum(t.jumlah for t in pemasukan)
    total_pengeluaran = sum(p.jumlah for p in pengeluaran)

    return render_template(
        "laporan_cabang.html",
        materials=Material.query.all(),
        transaksi=pemasukan,
        transaksi_pagination=pemasukan_pagination,
        pengeluaran=pengeluaran,
        total_pemasukan=total_pemasukan,
        total_pengeluaran=total_pengeluaran,
        tanggal=tanggal
    )
# ================= TUTUP LAPORAN =================
@app.route('/tutup_laporan')
@login_required
def tutup_laporan():

    if current_user.role != "cabang":
        return redirect(url_for('dashboard'))

    tanggal = request.args.get('tanggal')
    tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")

    data = Keuangan.query.filter_by(
        cabang=current_user.cabang,
        tanggal=tanggal_obj,
        status="Draft"
    ).all()

    for d in data:
        d.status = "Final"

    db.session.commit()

    flash("Laporan berhasil ditutup dan dikunci", "success")
    # reset session laporan
    session.pop("laporan_tanggal", None)
    session.pop("edit_mode", None)

    return redirect(url_for('dashboard'))

# ================= ADMIN LAPORAN =================
@app.route('/laporan')
@login_required
def laporan():

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    tanggal = request.args.get('tanggal')
    cabang = request.args.get('cabang')
    page = request.args.get('page', 1, type=int)

    query = Keuangan.query.filter(
        Keuangan.status == "Final"
    )

    if tanggal:
        try:
            tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d").date()
            query = query.filter(Keuangan.tanggal == tanggal_obj)
        except ValueError:
            flash("Format tanggal salah")

    if cabang:
        query = query.filter(Keuangan.cabang == cabang)

    # ambil semua data
    data = query.all()

    # ================= GROUP BY CABANG + TANGGAL =================
    laporan_dict = {}

    for d in data:
        key = (d.cabang, d.tanggal)

        if key not in laporan_dict:
            laporan_dict[key] = {
                "cabang": d.cabang,
                "tanggal": d.tanggal,
                "total_pemasukan": 0,
                "total_pengeluaran": 0
            }

        if d.tipe == "pemasukan":
            laporan_dict[key]["total_pemasukan"] += d.jumlah

        elif d.tipe == "pengeluaran":
            laporan_dict[key]["total_pengeluaran"] += d.jumlah

    laporan_list = list(laporan_dict.values())

    # ================= SORT TERBARU =================
    laporan_list.sort(key=lambda x: x["tanggal"], reverse=True)

    # ================= PAGINATION MANUAL =================
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    data_page = laporan_list[start:end]

    total_pages = (len(laporan_list) + per_page - 1) // per_page

    class Pagination:
        def __init__(self, page, total_pages):
            self.page = page
            self.pages = total_pages
            self.has_prev = page > 1
            self.has_next = page < total_pages

        def prev_num(self):
            return self.page - 1

        def next_num(self):
            return self.page + 1

    pagination = Pagination(page, total_pages)

    if tanggal and not data_page:
        flash("Tidak ada laporan pada tanggal tersebut")

    return render_template(
        "laporan_list.html",
        data=data_page,
        pagination=pagination,
        tanggal=tanggal,
        cabang=cabang
    )
# ================= DETAIL LAPORAN =================
@app.route('/laporan_detail')
@login_required
def laporan_detail():

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    cabang = request.args.get("cabang")
    tanggal = request.args.get("tanggal")

    if not cabang or not tanggal:
        return redirect(url_for('laporan'))

    tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d").date()

    # ================= PEMASUKAN =================
    page_transaksi = request.args.get('page_transaksi', 1, type=int)

    transaksi_pagination = Keuangan.query.filter(
        Keuangan.cabang == cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pemasukan",
        Keuangan.status == "Final"
    ).order_by(Keuangan.id.desc()).paginate(
        page=page_transaksi,
        per_page=10,
        error_out=False
    )

    transaksi = transaksi_pagination.items

    # ================= PENGELUARAN =================
    page_pengeluaran = request.args.get('page_pengeluaran', 1, type=int)

    pengeluaran_pagination = Keuangan.query.filter(
        Keuangan.cabang == cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pengeluaran",
        Keuangan.status == "Final"
    ).order_by(Keuangan.id.desc()).paginate(
        page=page_pengeluaran,
        per_page=10,
        error_out=False
    )

    pengeluaran = pengeluaran_pagination.items

    # ================= TOTAL =================
    total_pemasukan = db.session.query(
        db.func.sum(Keuangan.jumlah)
    ).filter(
        Keuangan.cabang == cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pemasukan",
        Keuangan.status == "Final"
    ).scalar() or 0

    total_pengeluaran = db.session.query(
        db.func.sum(Keuangan.jumlah)
    ).filter(
        Keuangan.cabang == cabang,
        Keuangan.tanggal == tanggal_obj,
        Keuangan.tipe == "pengeluaran",
        Keuangan.status == "Final"
    ).scalar() or 0

    # ================= DATA LAPORAN =================
    laporan = {
        "cabang": cabang,
        "tanggal": tanggal_obj,
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran
    }

    return render_template(
        "laporan_detail.html",
        laporan=laporan,
        transaksi=transaksi,
        transaksi_pagination=transaksi_pagination,
        pengeluaran=pengeluaran,
        pengeluaran_pagination=pengeluaran_pagination
    )
# ================= TAMBAH STOK PUSAT =================
@app.route('/tambah_stok', methods=['GET','POST'])
@login_required
def tambah_stok():

    if current_user.role != "admin":
        return redirect(url_for('dashboard'))

    if request.method == "POST":

        material_id = int(request.form['material'])
        jumlah = float(request.form['jumlah'])

        stok = StokCabang.query.filter_by(
            material_id=material_id,
            lokasi="Pusat"
        ).first()

        if stok:
            stok.total_kubik = round(stok.total_kubik + jumlah, 2)

        else:
            stok = StokCabang(
                material_id=material_id,
                lokasi="Pusat",
                total_kubik=round(jumlah, 2)
            )

            db.session.add(stok)

        db.session.commit()

        flash("Stok pusat berhasil ditambahkan", "success")

        return redirect(url_for('tambah_stok'))

    data = StokCabang.query.filter_by(
        lokasi="Pusat"
    ).all()

    return render_template(
        "tambah_stok.html",
        materials=Material.query.all(),
        data=data
    )
# ================= PDF =================
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

@app.route('/laporan_pdf')
@login_required
def laporan_pdf():

    cabang = request.args.get('cabang')
    tanggal = request.args.get('tanggal')
    tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")

    # ================= DATA KEUANGAN =================

    transaksi = Keuangan.query.filter_by(
        cabang=cabang,
        tanggal=tanggal_obj,
        tipe="pemasukan",
        status="Final"
    ).all()

    pengeluaran = Keuangan.query.filter_by(
        cabang=cabang,
        tanggal=tanggal_obj,
        tipe="pengeluaran",
        status="Final"
    ).all()

    total_pemasukan = sum(t.jumlah for t in transaksi)
    total_pengeluaran = sum(p.jumlah for p in pengeluaran)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=60
    )

    elements = []
    styles = getSampleStyleSheet()

    # ================= HEADER STYLE =================
    title_style = ParagraphStyle(
        name="TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0d3b66"),
        spaceAfter=10
    )

    # ================= TITLE =================
    elements.append(Paragraph("PT SAMPURNA ABADI MAKMUR", title_style))
    elements.append(Paragraph("LAPORAN HARIAN MATERIAL", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(HRFlowable(width="100%", thickness=2,
                               color=colors.HexColor("#0d3b66")))
    elements.append(Spacer(1, 0.3 * inch))

    # ================= INFO TABLE =================
    info_data = [
        ["Cabang", cabang],
        ["Tanggal", tanggal]
    ]

    info_table = Table(info_data, colWidths=[120, 350])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ================= TRANSAKSI =================
    elements.append(Paragraph("TRANSAKSI", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    transaksi_data = [["No", "Material", "Truck", "Kubikasi", "Metode", "Total"]]

    for i, t in enumerate(transaksi, start=1):
        transaksi_data.append([
            str(i),
            t.material.nama,
            t.jenis_truck,
            f"{round(t.kubikasi,2)} m³",
            t.metode,
            f"Rp {format(int(t.jumlah), ',').replace(',', '.')}"
        ])

    transaksi_table = Table(transaksi_data,
                            colWidths=[30, 100, 100, 70, 70, 100])

    transaksi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d3b66")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.transparent])
    ]))

    elements.append(transaksi_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ================= PENGELUARAN =================
    elements.append(Paragraph("PENGELUARAN", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    pengeluaran_data = [["No", "Keterangan", "Jumlah"]]

    for i, p in enumerate(pengeluaran, start=1):
        pengeluaran_data.append([
            str(i),
            p.keterangan,
            f"Rp {format(int(p.jumlah), ',').replace(',', '.')}"
        ])

    pengeluaran_table = Table(pengeluaran_data,
                              colWidths=[40, 300, 130])

    pengeluaran_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#198754")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.transparent])
    ]))

    elements.append(pengeluaran_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ================= TOTAL BOX =================
    total_data = [
        ["Total Pemasukan",
         f"Rp {format(int(total_pemasukan), ',').replace(',', '.')}"],
        ["Total Pengeluaran",
         f"Rp {format(int(total_pengeluaran), ',').replace(',', '.')}"]
    ]

    total_table = Table(total_data, colWidths=[250, 220])

    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#e9ecef")),
        ('GRID', (0, 0), (-1, -1), 0.6, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0d3b66")),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor("#b02a37"))
    ]))

    elements.append(total_table)

    # ================= FOOTER FUNCTION =================
    def add_page_design(canvas, doc):
        canvas.saveState()

        width, height = A4

        # ================= BACKGROUND COLOR =================
        canvas.setFillColor(colors.HexColor("#f8f9fa"))  # soft light grey
        canvas.rect(0, 0, width, height, stroke=0, fill=1)

        # ================= BORDER FRAME =================
        canvas.setStrokeColor(colors.HexColor("#0d3b66"))
        canvas.setLineWidth(2)
        canvas.rect(15, 15, width - 30, height - 30, stroke=1, fill=0)

        # ================= HEADER BAR =================
        canvas.setFillColor(colors.HexColor("#0d3b66"))
        canvas.rect(15, height - 60, width - 30, 35, stroke=0, fill=1)

        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(30, height - 45,
                          "PT SAMPURNA ABADI MAKMUR")

        # ================= FOOTER =================
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)

        footer_text = f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        page_number_text = f"Page {doc.page}"

        canvas.drawString(40, 25, footer_text)
        canvas.drawRightString(width - 40, 25, page_number_text)

        canvas.restoreState()

    doc.build(elements,
              onFirstPage=add_page_design,
              onLaterPages=add_page_design)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"laporan_{cabang}_{tanggal}.pdf",
        mimetype='application/pdf'
    )
@app.route('/nota_kirim/<int:id>')
@login_required
def nota_kirim(id):

    kirim = KirimStok.query.get_or_404(id)
    material = Material.query.get(kirim.material_id)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(700, 400),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # ================= STYLE =================
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=colors.HexColor("#0d3b66"),
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=20
    )

    normal_style = styles["Normal"]

    total_style = ParagraphStyle(
        name="Total",
        parent=styles["Normal"],
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#0d3b66")
    )

    # ================= HEADER =================
    elements.append(Paragraph("PT SAMPURNA ABADI MAKMUR", title_style))
    elements.append(Paragraph("NOTA PENGIRIMAN MATERIAL", subtitle_style))

    # ================= INFO =================
    info_table = Table([
        ["No Nota", f": #{kirim.id}", "Tanggal", f": {kirim.tanggal.strftime('%d-%m-%Y')}"],
        ["Tujuan Pengiriman", f": Cabang {kirim.cabang}", "Dibuat Oleh", f": {current_user.username}"]
    ], colWidths=[120, 180, 100, 180])

    info_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # ================= TABEL =================
    data_table = Table([
        ["No", "Nama Material", "Jumlah Truck", "Total Kubikasi (m³)"],
        [
            "1",
            material.nama if material else "-",
            str(kirim.jumlah_truck),
            f"{round(kirim.total_kubik,2)}"
        ]
    ], colWidths=[50, 250, 150, 150])

    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0d3b66")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    elements.append(data_table)
    elements.append(Spacer(1, 25))

    # ================= TOTAL =================
    elements.append(Paragraph(
        f"TOTAL KUBIKASI: {round(kirim.total_kubik,2)} m³",
        total_style
    ))

    elements.append(Spacer(1, 30))

    # ================= FOOTER =================
    elements.append(Paragraph(
        "Dokumen ini merupakan bukti pengiriman material yang dibuat secara sistem.",
        styles["Italic"]
    ))

    # ================= BORDER FIX =================
    def draw_border(canvas, doc):
        canvas.saveState()

        width, height = doc.pagesize

        margin = 15

        # 🔥 BORDER LUAR RAPI
        canvas.setStrokeColor(colors.HexColor("#0d3b66"))
        canvas.setLineWidth(2)
        canvas.rect(
            margin,
            margin,
            width - (margin * 2),
            height - (margin * 2)
        )

        # 🔥 GARIS HEADER
        canvas.setStrokeColor(colors.grey)
        canvas.setLineWidth(1)
        canvas.line(
            margin + 20,
            height - 90,
            width - margin - 20,
            height - 90
        )

        canvas.restoreState()

    doc.build(elements, onFirstPage=draw_border)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"nota_kirim_{kirim.id}.pdf",
        mimetype='application/pdf'
    )
@app.route('/nota_transaksi/<int:id>')
@login_required
def nota_transaksi(id):

    transaksi = Keuangan.query.get_or_404(id)

    # 🔥 Proteksi akses
    if current_user.role == "cabang" and transaksi.cabang != current_user.cabang:
        return redirect(url_for('dashboard'))

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(700, 400),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # ================= STYLE =================
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=colors.HexColor("#0d3b66"),
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=20
    )

    total_style = ParagraphStyle(
        name="Total",
        parent=styles["Normal"],
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#0d3b66")
    )

    # ================= HEADER =================
    elements.append(Paragraph("PT SAMPURNA ABADI MAKMUR", title_style))
    elements.append(Paragraph("NOTA TRANSAKSI MATERIAL", subtitle_style))

    # ================= INFO =================
    info_table = Table([
        ["No Nota", f": #{transaksi.id}", "Tanggal", f": {transaksi.tanggal.strftime('%d-%m-%Y')}"],
        ["Cabang", f": {transaksi.cabang}", "Metode", f": {transaksi.metode or '-'}"],
        ["Dibuat Oleh", f": {current_user.username}", "", ""]
    ], colWidths=[120, 180, 100, 180])

    info_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # ================= TABEL =================
    data_table = Table([
        ["No", "Material", "Truck", "Kubikasi (m³)", "Total"],
        [
            "1",
            transaksi.material.nama if transaksi.material else "-",
            transaksi.jenis_truck or "-",
            f"{round(transaksi.kubikasi,2)}",
            f"Rp {format(int(transaksi.jumlah), ',').replace(',', '.')}"
        ]
    ], colWidths=[40, 180, 120, 120, 120])

    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0d3b66")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    elements.append(data_table)
    elements.append(Spacer(1, 25))

    # ================= TOTAL =================
    elements.append(Paragraph(
        f"TOTAL PEMBAYARAN: Rp {format(int(transaksi.jumlah), ',').replace(',', '.')}",
        total_style
    ))

    elements.append(Spacer(1, 30))

    # ================= FOOTER =================
    elements.append(Paragraph(
        "Nota ini merupakan bukti transaksi resmi dari sistem.",
        styles["Italic"]
    ))

    # ================= BORDER =================
    def draw_border(canvas, doc):
        canvas.saveState()

        width, height = doc.pagesize
        margin = 15

        canvas.setStrokeColor(colors.HexColor("#0d3b66"))
        canvas.setLineWidth(2)
        canvas.rect(margin, margin, width - (margin * 2), height - (margin * 2))

        canvas.setStrokeColor(colors.grey)
        canvas.setLineWidth(1)
        canvas.line(margin + 20, height - 90, width - margin - 20, height - 90)

        canvas.restoreState()

    doc.build(elements, onFirstPage=draw_border)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"nota_transaksi_{transaksi.id}.pdf",
        mimetype='application/pdf'
    )
# ================= RESET PASSWORD =================
@app.route('/reset_password', methods=['POST'])
@login_required
def reset_password():

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    if current_user.password != old_password:
        flash("Password lama salah", "danger")
        return redirect(request.referrer)

    current_user.password = new_password
    db.session.commit()

    flash("Password berhasil diperbarui", "success")
    return redirect(request.referrer)


@app.context_processor
def inject_notifikasi():
    jumlah_notif = 0
    stok_menipis = []
    stok_menipis_all = []

    if current_user.is_authenticated:

        # ================= NOTIF KONFIRMASI STOK =================
        if current_user.role == "cabang":
            jumlah_notif = KirimStok.query.filter_by(
                cabang=current_user.cabang,
                status="Menunggu"
            ).count()

        # ================= STOK MENIPIS CABANG =================
        if current_user.role == "cabang":
            stok_menipis = db.session.query(
                StokCabang,
                Material.nama
            ).join(
                Material, Material.id == StokCabang.material_id
            ).filter(
                StokCabang.lokasi == current_user.cabang,
                StokCabang.total_kubik < 30
            ).all()

        # ================= STOK MENIPIS ADMIN =================
        elif current_user.role == "admin":
            stok_menipis_all = db.session.query(
                StokCabang,
                Material.nama
            ).join(
                Material, Material.id == StokCabang.material_id
            ).filter(
                StokCabang.total_kubik < 30,
                StokCabang.lokasi != "Pusat"
            ).all()

    return dict(
        notifikasi_stok=jumlah_notif,
        stok_menipis=stok_menipis,
        stok_menipis_all=stok_menipis_all
    )

if __name__ == "__main__":
    app.run(debug=True)
