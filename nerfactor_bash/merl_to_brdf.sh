start_time="$(date -u +%s)"

proj_root='/home/jiwonchoi'
repo_dir="$proj_root/nerfactor"
indir="$proj_root/data/brdf_merl/brdfs"
ims='512'
outdir="$proj_root/data/brdf_merl_npz/ims${ims}_envmaph16_spp1"
REPO_DIR="$repo_dir" "$repo_dir"/data_gen/merl/make_dataset_run.sh "$indir" "$ims" "$outdir"

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo ""
echo "Seconds elapsed: $elapsed"
