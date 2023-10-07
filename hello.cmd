
curl.exe -X POST -H "Content-Type: application/json" -d '{
    \"title\": \"Song\",
    \"genre\": \"song\",
    \"artist\": \"karthik\",
    \"duration\": \"3:30\" 
}' http://localhost:5000/music

curl.exe -X POST -H "Content-Type: application/json" -d '{
    \"title\": \"Song2\",
    \"genre\": \"song23\",
    \"artist\": \"mahesh\",
    \"duration\": \"2:52\" 
}' http://localhost:5000/music

