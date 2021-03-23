stty -F $1 9600
exec 3<> $1
sleep 4
cat<&3
sleep 1
echo "manual_connect">&3
sleep 1
cat<&3
sleep 1
echo "dados">&3
sleep 10
cat<&3
exec 3>&-
