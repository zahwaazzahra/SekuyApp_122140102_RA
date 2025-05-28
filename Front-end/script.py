import os

def extract_frontend_code_to_md(src_folder='src', output_file='context.md'):
    """
    Mengekstrak isi semua file dari folder src frontend Vite
    dan menulisnya ke dalam satu file Markdown.
    """
    print(f"Mengekstrak kode dari '{src_folder}' ke '{output_file}'...")

    if not os.path.isdir(src_folder):
        print(f"Error: Folder '{src_folder}' tidak ditemukan. Pastikan Anda menjalankan script ini dari root project Vite Anda.")
        return

    # List ekstensi file yang biasanya relevan untuk frontend (bisa disesuaikan)
    relevant_extensions = ('.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.css', '.scss', '.less', '.html', '.json', '.mjs', '.cjs')

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Tulis header atau informasi awal
        outfile.write(f"# Frontend Code Context from '{src_folder}'\n\n")
        outfile.write(f"This document contains the consolidated code from the '{src_folder}' directory.\n")
        outfile.write("It is intended for AI context or documentation purposes.\n\n")
        outfile.write("---\n\n")

        for root, _, files in os.walk(src_folder):
            for filename in files:
                # Lewati file yang tidak relevan (contoh: asset gambar, file build, dll.)
                if not filename.endswith(relevant_extensions):
                    continue

                filepath = os.path.join(root, filename)
                relative_filepath = os.path.relpath(filepath, src_folder)

                print(f"  Memproses: {relative_filepath}")
                outfile.write(f"## File: `{relative_filepath}`\n\n")
                outfile.write("```\n") # Gunakan backtick tunggal untuk blok kode tanpa syntax highlighting spesifik

                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    outfile.write("\n```\n\n")
                except Exception as e:
                    outfile.write(f"```\nError reading file: {e}\n```\n\n")
                    print(f"    Gagal membaca file {filepath}: {e}")

    print(f"\nEkstraksi selesai! Output tersedia di '{output_file}'.")

if __name__ == "__main__":
    extract_frontend_code_to_md()