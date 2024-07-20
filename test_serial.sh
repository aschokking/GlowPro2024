testArr=("1" "2" "3" "4" "31" "32" "33" "34")
for i in ${!testArr[@]}; do
    echo "${testArr[$i]}"
    if [ "$i" -ge "${#testArr[@]}" ]; then
        i=0
    fi
done