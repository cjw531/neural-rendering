start_time="$(date -u +%s)"

gpus='2'
scene='pinecone'
proj_root='/home/jiwonchoi'
repo_dir="$proj_root/nerfactor"
scene_dir="$proj_root/data/nerf_real_360/$scene"
h='512'
n_vali='2'
outroot="$proj_root/data/nerf_real_360_proc/${scene}"
REPO_DIR="$repo_dir" "$repo_dir/data_gen/nerf_real/make_dataset_run.sh" --scene_dir="$scene_dir" --h="$h" --n_vali="$n_vali" --outroot="$outroot"

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo ""
echo "Seconds elapsed: $elapsed"
