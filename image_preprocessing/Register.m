fixedpoints = zeros(6,2);
movingpoints = zeros(6,2);
%% Read markers into markerArray
for n = 1:6
    markerArray{n} = rgb2gray(imread(sprintf('%01i.tif',n)));
end
%%
grayfixed = rgb2gray(imread('306.tif'));
rgbfixed = imread('306.tif');
for k = 1:6
    c = normxcorr2(markerArray{k},grayfixed);
    [ypeak, xpeak] = find(c==max(c(:)));
    fixedpoints(k,:) = [xpeak, ypeak];
end
image0_ref = imref2d(size(rgbfixed));
    %%
for n = 87:88
    %n = 29*2*i+1
    movingpoints = zeros(6,2);
    graymoving = rgb2gray(imread(sprintf('%01i.tif',n)));
    rgbmoving = imread(sprintf('%01i.tif',n));
    for k = 1:6
        c = normxcorr2(markerArray{k},graymoving);
        [ypeak, xpeak] = find(c==max(c(:)));
        movingpoints(k,:) = [xpeak, ypeak];
    end
    t_image = fitgeotrans(movingpoints,fixedpoints,'projective');
    %t_image = fitgeotrans(movingpoints,fixedpoints,'affine');
    image1_registered = imwarp(rgbmoving,t_image,'OutputView',image0_ref);
    name = num2str(n);
    imwrite(image1_registered, [name, 'reg.png'])
end

%%  Or manually select points and register; load images
imagefixed = imread('306.tif');
imagemoving = imread('523.tif');
%% manually select points and register; select points
h  = cpselect(imagemoving,imagefixed);
%initialMovingPoints = movingPoints;
%initialFixedPoints = fixedPoints;
%h = cpselect(imagemoving,imagefixed,initialMovingPoints,initialFixedPoints);
%close h;
%% manually select points and register; calculate
t_image = fitgeotrans(movingPoints1,fixedPoints1,'projective');

imagefixed_ref = imref2d(size(imagefixed)); %relate intrinsic and world coordinates
imagemoving_registered = imwarp(imagemoving,t_image,'OutputView',imagefixed_ref); % Perform perspective transformation
imwrite(imagemoving_registered, '523reg.png') % Export registered image
%clear all;