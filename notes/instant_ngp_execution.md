# Neural Rendering Updates (August 16, 2022)

## `instant-ngp` Execution
1. Run COLMAP
```
sudo nvidia-docker run -v /home/jiwon/workspace:/mnt/foo -it geki/colmap
```

2. Go to `./mnt/foo/<IMG_FOLDER>` once logged into the Docker container

3. Run the python file that has COLMAP commands
```
python3 ../colmap_runner.py
```

4. Check `sparse/0` folder after COLMAP execution. If `sparse` folder has multiple indexed sub-folders, or `sparse/0` does not have all the images, then the COLMAP has failed.

5. Come back to the local terminal, run pre-processing in local's `<IMG_FOLDER>`. Make sure to activate conda environment `ngp`.
```
../../instant-ngp/scripts/colmap2nerf.py --aabb_scale 4
```
`aabb_scale` here indicates the size of the bounding box. It provides a limit in 3D rendered space, up to in which part that you would like to ask the renderer to render/include.

Sample successful output:
```
up vector was [-0.99982943 -0.00361648  0.01811169]
computing center of attention...
[-176.18570428    6.07780515   -0.21637626]
avg camera distance from origin 176.39161056529872
60 frames
writing transforms.json
```

6. Run `instant-ngp` for NeRF in a folder where `instant-ngp` repository is located & `ngp` conda environment should be activated:
```
./build/testbed --mode nerf --scene ../img_dataset/<IMG_FOLDER>/
```
