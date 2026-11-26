# The score repair

A cube point is a predictor on three equally likely input points, with coordinates g1, g2 and g3. The groups {1, 2} and {2, 3} impose two linear equations. The purple segment contains the original feasible scores. The gold diamond is f = (3/4, 1/4, 1). When the third point's label mean grows, the green feasible line shifts and its endpoint stays on g3 = 1.

At the largest illustrated shift, the last label mean moves from 3/4 to 7/8. The nearest repair is (5/8, 3/8, 1). Its mean absolute change is (1/8 + 1/8)/3 = 1/12. For a label increase of t/4 the distance is t/6. The line and points show the true means in this teaching example.

Extract the ZIP and open index.html. Use the label slider to change the last label mean, and drag the cube horizontally or move the rotation slider. Every fraction is displayed exactly.

Run `python3 visualization/render.py` with Pillow and Arial fonts to rebuild the GIF and ZIP. Set `Q572_FONT_DIR` to the folder containing Arial.ttf and Arial Bold.ttf if they are elsewhere. The standard-library repository replay independently checks all nine explorer positions.
