from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# memastikan folder upload ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# koneksi MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["db_minimarket"]
collection = db["barang"]


# INDEX
@app.route('/')
def index():
    data = list(collection.find())
    return render_template("index.html", data=data)



# ADD BARANG
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form.get('kategori')

        # upload gambar
        file = request.files['gambar']
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # simpan ke database
        collection.insert_one({
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "stok": stok,
            "kategori": kategori,
            "gambar": filename
        })

        return redirect(url_for('index'))

    return render_template('add.html')


# EDIT BARANG

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':

        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form.get('kategori')

        # gambar lama
        old_image = item.get('gambar')
        filename = old_image

        # Cek apakah user upload gambar baru
        file = request.files['gambar']
        if file and file.filename != "":
            # Hapus file lama jika ada
            if old_image and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], old_image)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_image))

            # Simpan file baru
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # update database
        collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                "kode": kode,
                "nama": nama,
                "harga": harga,
                "stok": stok,
                "kategori": kategori,
                "gambar": filename
            }}
        )

        return redirect(url_for('index'))

    return render_template('edit.html', item=item)



# DELETE BARANG

@app.route('/delete/<id>')
def delete(id):
    item = collection.find_one({'_id': ObjectId(id)})

    # hapus gambar dari folder
    if item and item.get("gambar"):
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], item["gambar"])
        if os.path.exists(img_path):
            os.remove(img_path)

    # hapus dari database
    collection.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('index'))


# RUN

if __name__ == '__main__':
    app.run(debug=True)
