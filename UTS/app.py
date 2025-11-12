from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dijahaechan'  # ganti kalau beda
app.config['MYSQL_DB'] = 'rumah_sakit'

mysql = MySQL(app)

# --------------------- ROUTE: INDEX ---------------------
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id_pasien, p.nama_pasien, p.nomor_antrian, pl.nama_poli, pl.dokter, pl.jadwal_praktik
        FROM pasien p
        JOIN poliklinik pl ON p.kode_poli = pl.kode_poli
    """)
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', pasien=data)

# --------------------- ROUTE: TAMBAH ---------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM poliklinik")
    poliklinik = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        id_pasien = request.form['id_pasien']
        nama_pasien = request.form['nama_pasien']
        nomor_antrian = request.form['nomor_antrian']
        kode_poli = request.form['kode_poli']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO pasien (id_pasien, nama_pasien, nomor_antrian, kode_poli)
            VALUES (%s, %s, %s, %s)
        """, (id_pasien, nama_pasien, nomor_antrian, kode_poli))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('add.html', poliklinik=poliklinik)

# --------------------- ROUTE: EDIT ---------------------
@app.route('/edit/<id_pasien>', methods=['GET', 'POST'])
def edit(id_pasien):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM poliklinik")
    poliklinik = cur.fetchall()

    cur.execute("SELECT * FROM pasien WHERE id_pasien = %s", (id_pasien,))
    pasien = cur.fetchone()

    if request.method == 'POST':
        nama_pasien = request.form['nama_pasien']
        nomor_antrian = request.form['nomor_antrian']
        kode_poli = request.form['kode_poli']

        cur.execute("""
            UPDATE pasien
            SET nama_pasien=%s, nomor_antrian=%s, kode_poli=%s
            WHERE id_pasien=%s
        """, (nama_pasien, nomor_antrian, kode_poli, id_pasien))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    cur.close()
    return render_template('edit.html', pasien=pasien, poliklinik=poliklinik)

# --------------------- ROUTE: HAPUS ---------------------
@app.route('/delete/<id_pasien>')
def delete(id_pasien):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pasien WHERE id_pasien=%s", (id_pasien,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
