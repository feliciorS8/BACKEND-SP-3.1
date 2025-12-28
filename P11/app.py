from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfigurasi upload
UPLOAD_FOLDER = 'assets/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# koneksi database
def db():
    conn = sqlite3.connect("tokoBaju.db")
    conn.row_factory = sqlite3.Row
    return conn

# membuat tabel jika belum ada
def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS produk(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT NOT NULL,
            nama TEXT NOT NULL,
            ukuran TEXT NOT NULL,
            warna TEXT NOT NULL,
            stok INTEGER NOT NULL,
            harga REAL NOT NULL,
            gambar TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# read
@app.route("/")
def index():
    conn = db()
    rows = conn.execute("SELECT * FROM produk").fetchall()
    conn.close()
    return render_template("index.html", stoks=rows)

# create 
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        ukuran = request.form["ukuran"]
        warna = request.form["warna"]
        stok = request.form["stok"]
        harga = request.form["harga"]
        
        # Handle upload gambar
        gambar_filename = None
        if 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Buat nama unik
                filename = f"{kode}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                gambar_filename = filename
        
        conn = db()
        conn.execute("INSERT INTO produk (kode, nama, ukuran, warna, stok, harga, gambar) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                     (kode, nama, ukuran, warna, stok, harga, gambar_filename))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# update
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = db()
    Stok = conn.execute("SELECT * FROM produk WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        ukuran = request.form["ukuran"]
        warna = request.form["warna"]
        stok = request.form["stok"]
        harga = request.form["harga"]
        
        # Handle upload gambar baru
        gambar_filename = Stok['gambar']  # Keep old image
        if 'gambar' in request.files:
            file = request.files['gambar']
            if file and file.filename != '' and allowed_file(file.filename):
                # Hapus gambar lama jika ada
                if Stok['gambar']:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], Stok['gambar'])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                filename = f"{kode}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                gambar_filename = filename
        
        conn.execute("UPDATE produk SET kode=?, nama=?, ukuran=?, warna=?, stok=?, harga=?, gambar=? WHERE id=?", 
                     (kode, nama, ukuran, warna, stok, harga, gambar_filename, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    conn.close()
    return render_template("edit.html", stoks=Stok)

# delete
@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    row = conn.execute("SELECT gambar FROM produk WHERE id=?", (id,)).fetchone()
    
    # Hapus gambar jika ada
    if row and row['gambar']:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], row['gambar'])
        if os.path.exists(img_path):
            os.remove(img_path)
    
    conn.execute("DELETE FROM produk WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)