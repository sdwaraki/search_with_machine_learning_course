# A simple loop that can be run to check on counts for our two indices as you are indexing.  Ctrl-c to get out.
while [ true ];
do
  echo "Products:"
  curl -k -XGET -u admin:admin  "https://localhost:9200/_cat/count/bbuy_products";
  sleep 60;
done