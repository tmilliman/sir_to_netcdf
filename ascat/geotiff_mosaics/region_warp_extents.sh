
case ${region} in
    'Ala')
        warp_extent="-179.5 50.5 -132.5 70.0"
        ;;
    'NAm')
        warp_extent="-132.5 27.5 -52.5 64.5"
        ;;
    'CAm')
        warp_extent="-114.5 5.5 -57.5 27.5"
        ;;
    'SAm')
        warp_extent="-82.5. -56.5 -32.5 14.5"
        ;;
    'NAf')
        warp_extent="-19.5 2.5 62.5 39.5"
        ;;
    'SAf')
        warp_extent="5.5 -37.5 52.5 2.5"
        ;;
    'Sib')
        warp_extent="64. 50.1 179.5 70."
        ;;
    'Eur')
        warp_extent="-12. 39.5 64. 70."
        ;;
    'SAs')
        warp_extent="62.5 5.5 150. 27.5"
        ;;
    'ChJ')
        warp_extent="60. 27.5 150. 52.5"
        ;;
    'Ind')
        warp_extent="93. -12. 165. 5.5"
        ;;
    'Aus')
        warp_extent="110. -47. 179. -12."
        ;;
    'Grn')
        warp_extent="-74. 59. -11. 70."
        ;;
    'Ber')
        # split into to images since region spands anti-meridian
        warp_extent1="135.5 48.5 179.9 70.0"
        warp_extent2="-179.90 48.5 -136.5 70.0"
        ;;
    *)
        echo "Unknown region extent"
        exit
esac
if [ ${region} == "Ber" ]
then
    echo ${warp_extent1}
    echo ${warp_extent2}
else
    echo ${warp_extent}
fi
