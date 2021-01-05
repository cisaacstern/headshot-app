# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
import panel as pn
from panel.template.theme import DarkTheme
pn.extension()

react = pn.template.ReactTemplate(title='Headshot', theme=DarkTheme)
#canvas = react.theme.bokeh_theme._json['attrs']['ColorBar']['background_fill_color']
canvas = '#121212'
pn.config.sizing_mode = 'scale_both'

sigma = pn.widgets.FloatSlider(name="Sigma", start=0, end=4, value=3)
levels = pn.widgets.IntSlider(name="Levels", start=0, end=10, value=3)

image = plt.imread('headshot.png')

# +
def plotter(Z, levels, cmap, image):
    fig, ax = plt.subplots()
    
    cont = ax.contourf(Z, levels=levels, origin='upper', cmap=cmap)
    
    x, y = image.shape[0]/2, image.shape[0]/2
    patch = patches.Circle((x, y), radius=y-10, transform=ax.transData)
    
    for col in cont.collections:
        col.set_clip_path(patch)
    
    fig.patch.set_facecolor(canvas)
    ax.axis('off')
    plt.axis('equal')
    plt.savefig("test.svg")
    plt.close()
    return fig

@pn.depends(sigma=sigma, levels=levels)
def headshot(sigma, levels, cmap='copper', 
             image=image, view_fn=plotter):

    Z = image[:,:,2]
    Z = gaussian_filter(Z, sigma=sigma)
    
    return view_fn(Z=Z, levels=levels, cmap=cmap,
                   image=image)

# -

canvas

headshot(sigma=3, levels=2)

react.sidebar.append(sigma)
react.sidebar.append(levels)

# Unlike other templates the `ReactTemplate.main` area acts like a GridSpec 
react.main[:4, :6] = headshot

react.servable();

