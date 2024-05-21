import zstandard as zstd
import os

input_file = r"C:\Users\fayaz\Desktop\og\UI\LayoutArchive\Menu.Product.100.Nin_NX_NVN.blarc"

output_file = f"{input_file}.zs"
cctx = zstd.ZstdCompressor()

with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
    compressed_data = cctx.compress(f_in.read())
    f_out.write(compressed_data)

compressed_filename = os.path.basename(output_file)

print(f"Compressed {compressed_filename}")