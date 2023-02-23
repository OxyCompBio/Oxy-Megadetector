# take Python cities as input
# and create subfolders for each city
# non-alphanumeric characters have been stripped away

# takes processed_cities.txt as input
# creates the folders in local directory structure as "output"
# run with ./make_city_folders.sh processed_cities.txt

while read -r line
do
        printf 'City: %s\n' "$line"
	mkdir "$line"
done < "$1"

