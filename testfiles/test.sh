
# Test handling of custom comment pattern (while reading)
proptool -b tpl -l pl -v -t "COM |-=> KEY SEP"

# Test using custom comment pattern (while writing)
rm tplwrite_pl.properties
proptool -b tplwrite -l pl -v -t "COM |-=> KEY SEP" --fix
