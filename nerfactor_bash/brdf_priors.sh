start_time="$(date -u +%s)"

gpus='2'
# I. Learning BRDF Priors (training and validation)
proj_root='/home/jiwonchoi'
repo_dir="$proj_root/nerfactor"
data_root="$proj_root/data/brdf_merl_npz/ims256_envmaph16_spp1"
outroot="$proj_root/output/train/merl" 
viewer_prefix='' # or just use ''
REPO_DIR="$repo_dir" "$repo_dir/nerfactor/trainvali_run.sh" "$gpus" --config='brdf.ini' --config_override="data_root=$data_root,outroot=$outroot,viewer_prefix=$viewer_prefix"

# II. Exploring the Learned Space (validation and testing)
ckpt="$outroot/lr1e-2/checkpoints/ckpt-50"
REPO_DIR="$repo_dir" "$repo_dir/nerfactor/explore_brdf_space_run.sh" "$gpus" --ckpt="$ckpt"

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo ""
echo "Seconds elapsed: $elapsed"
