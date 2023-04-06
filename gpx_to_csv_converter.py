from gpx_converter import Converter

Gpx=input('Enter the GPX file name with .gpx: ')
Csv=input('Enter the name of the output CSV with .csv : ')

Converter(input_file=Gpx).gpx_to_csv(output_file=Csv)