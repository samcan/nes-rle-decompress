import argparse
import os

MAX_BYTE_COUNT = 255

def main(input_file, output_file):
    print('Input file:', input_file)
    print('Output file:', output_file)
    if os.path.isfile(output_file):
        os.remove(output_file)

    with open(input_file, 'rb') as f:
        bytes_read = f.read()
        
        prev_byte = ''
        count = 0
        for byte in bytes_read:
            if prev_byte == '':
                prev_byte = byte
                count = 1
            elif byte == prev_byte:
                count += 1
            
            # I may modify this at some point to use negative
            # numbers to represent a list of bytes which should
            # be copied as-is. For example, a count of -6 would mean
            # that the next six bytes should be copied as-is.
            #
            # I could convert a negative number n to an 8-bit two's complement
            # number for conversion to hex by doing the following per the Wikipedia
            # article:
            #
            # = 2^8 - n
            #
            # For n = -5
            # = 2^8 - 5
            # = 251
            #
            # This means I would need to limit the following count to 127
            if count == MAX_BYTE_COUNT:
                write_byte(output_file, count, prev_byte)
                prev_byte = byte
                count = 0
                
            if byte != prev_byte:
                write_byte(output_file, count, prev_byte)
                
                #print('setting prev_byte to',byte)
                prev_byte = byte
                count = 1
                
        
        # write final byte to file
        write_byte(output_file, count, prev_byte)
        
        # tack on terminating #$00 bytes
        write_byte(output_file, 0, 0)
    
    # print file compression info
    input_file_num_bytes = os.stat(input_file).st_size
    output_file_num_bytes = os.stat(output_file).st_size
    
    print('Input file size (bytes):', input_file_num_bytes)
    print('Output file size (bytes):', output_file_num_bytes)
    compression_pct = 1 - (output_file_num_bytes / input_file_num_bytes)
    print(f"Compression (%): {compression_pct * 100:.1f}")
    print()

def write_byte(output, count, byte):
    #print('writing',count,'of',bytes([byte]))
    with open(output, 'ba') as g:
        g.write(bytes([count]))
        g.write(bytes([byte]))

parser = argparse.ArgumentParser(description='Take bin file and RLE encode it.')
parser.add_argument('--input', required=True, type=str, help='Input bin file')
parser.add_argument('--output', required=True, type=str, help='Output bin file')
args = parser.parse_args()

main(args.input, args.output)