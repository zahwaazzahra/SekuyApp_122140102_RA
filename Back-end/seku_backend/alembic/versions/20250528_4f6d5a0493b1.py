# alembic/versions/<your_migration_file_id>.py

"""second

Revision ID: 4f6d5a0493b1
Revises: 1a41e7bb9051
Create Date: 2025-05-28 16:25:02.825633

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from passlib.hash import pbkdf2_sha256 # IMPORT passlib di sini juga!

# revision identifiers, used by Alembic.
revision = '4f6d5a0493b1'
down_revision = '1a41e7bb9051'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add the new column as nullable=True
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True)) # UBAH JADI NULLABLE=TRUE

    # Step 2: Populate existing rows with a default password_hash (atau hash ulang password lama jika ada)
    # Ini sangat penting! Tanpa ini, akan tetap ada NULL.
    # Kita akan membuat password_hash default untuk user yang sudah ada.
    # PENTING: Jika Anda punya kolom 'password' lama yang berisi plain text,
    # sebaiknya hash kolom 'password' lama itu dan pindahkan ke 'password_hash'.
    # Karena Anda mengubah nama kolom dari 'password' menjadi 'password_hash' di model,
    # dan sepertinya migrasinya hanya ADD COLUMN 'password_hash',
    # ini berarti kolom 'password' lama masih ada di database.
    # Jadi, kita perlu pindahkan dan hash isinya.

    # 1. Buat representasi tabel `users` untuk operasi DML
    users_table = table(
        'users',
        column('id', sa.BigInteger),
        column('password', sa.String(length=255)), # Kolom password lama
        column('password_hash', sa.String(length=255))
    )

    # 2. Ambil semua user yang sudah ada (hanya ID dan password lama)
    conn = op.get_bind()
    results = conn.execute(sa.text("SELECT id, password FROM users WHERE password_hash IS NULL;")).fetchall()

    # 3. Hash password lama dan update kolom password_hash
    for user_id, old_password in results:
        # PENTING: Anda harus memiliki nilai 'password' lama di database!
        # Jika kolom 'password' lama dihapus atau kosong, ini akan menyebabkan error.
        # Jika kolom 'password' lama sudah dihapus, Anda harus menyediakan nilai default atau null.
        if old_password is not None:
            hashed_password = pbkdf2_sha256.hash(old_password)
            op.execute(
                users_table.update().
                where(users_table.c.id == user_id).
                values(password_hash=hashed_password)
            )
        else:
            # Jika old_password is None atau tidak ada, Anda perlu putuskan
            # apakah akan memberikan hash untuk password default atau membiarkannya NULL
            # untuk kemudian diisi manual. Untuk saat ini, kita bisa set ke hash dari string kosong
            # atau string default lainnya jika Anda ingin semua user memiliki hash.
            # Ini sangat tergantung pada bagaimana data lama Anda.
            # Contoh: set ke hash dari 'default_password' jika old_password null
            default_hashed_password = pbkdf2_sha256.hash("default_password")
            op.execute(
                users_table.update().
                where(users_table.c.id == user_id).
                values(password_hash=default_hashed_password)
            )


    # Step 3: Alter the column to nullable=False (NOT NULL)
    op.alter_column('users', 'password_hash',
               existing_type=sa.String(length=255),
               nullable=False,
               existing_nullable=True)

    # Opsional: Jika Anda ingin menghapus kolom 'password' lama setelah migrasi
    # Ini harus dilakukan setelah semua data dipindahkan ke 'password_hash'
    op.drop_column('users', 'password') # HAPUS BARIS INI JIKA ANDA TIDAK MENGHAPUS KOLOM 'password' LAMA
    # Pastikan Anda sudah punya migrasi yang menambahkan 'password_hash' dan menghapus 'password'
    # Jika migrasi sebelumnya hanya mengganti tipe password ke string biasa, ini bisa kompleks.

def downgrade():
    # Opsional: Jika Anda menghapus kolom 'password' di upgrade, Anda mungkin ingin menambahkannya kembali di downgrade
    # op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))
    op.drop_column('users', 'password_hash')