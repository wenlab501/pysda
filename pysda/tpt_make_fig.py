
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from descartes import PolygonPatch # for drawing base polygon
from matplotlib.collections import PatchCollection
import seaborn as sns

def get_bounds(nodes, subclusters, prog_links):
    minx0, miny0, maxx0, maxy0 = list(nodes.total_bounds)
    minx1, miny1, maxx1, maxy1 = list(subclusters.total_bounds)
    minx2, miny2, maxx2, maxy2 = list(prog_links.total_bounds)
    minx = min(minx0, minx1, minx2)
    miny = min(miny0, miny1, miny2)
    maxx = max(maxx0, maxx1, maxx2)
    maxy = max(maxy0, maxy1, maxy2)
    return minx, miny, maxx, maxy

def get_top_groups(nodes, top_groups=5):
    chids = nodes['chid'].tolist()
    chidset = list(set(chids))
    counts = [ chids.count(c) for c in chidset ]
    ccset = sorted([ (co,ch) for co,ch in zip(counts,chidset) ], reverse=True)
    tops = []
    i = 0
    while len(tops)<top_groups:
        co,ch = ccset[i]
        ## -1 means not in a chain, nan means not in a subclsuter
        if (ch!='-1')and(not(np.isnan(ch))):
            tops.append(ch)
        i+=1
        if i>=len(chidset):
            print('Only {} chains are found, using {} subclusters to make figures.'.format(str(len(tops)), str(i-1)))
            break
    return tops

def get_nodes(nodes, tglist, colors, other_c='xkcd:light grey'):
    nodes2 = {'other':{'xx':[], 'yy':[], 'cc':other_c}}
    for g in tglist:
        nodes2[g] = {'xx':[], 'yy':[], 'cc':colors[tglist.index(g)]}
    chids = nodes['chid'].tolist()
    xx = nodes['xx'].tolist()
    yy = nodes['yy'].tolist()
    for ch,x,y in zip(chids, xx, yy):
        if ch in tglist:
            nodes2[ch]['xx'].append(x)
            nodes2[ch]['yy'].append(y)
        else:
            nodes2['other']['xx'].append(x)
            nodes2['other']['yy'].append(y)
    return nodes2

def get_subcs(subclusters, tglist, colors, other_c='xkcd:light grey'):
    subclusters2 = {'other':{'pc':[], 'c':other_c}}
    for g in tglist:
        subclusters2[g] = {'pc':[], 'c':colors[tglist.index(g)]}
    chids = subclusters['chid'].tolist()
    geoms = subclusters['geometry'].tolist()
    patches = []
    for i in range(len(chids)):
        ch = chids[i]
        geom = geoms[i]
        if ch in tglist:
            patch = PolygonPatch(geom, fc=colors[tglist.index(ch)], ec='0.5', zorder=4+tglist.index(ch), alpha=.7)
            subclusters2[ch]['pc'].append(patch)
        else:
            patch = PolygonPatch(geom, fc=other_c, ec='0.5', zorder=3, alpha=.7)
            subclusters2['other']['pc'].append(patch)
    subclusters3 = {}
    for k,v in subclusters2.items():
        patches = v['pc']
        pc2 = PatchCollection(patches, match_original=True)
        subclusters3[k] = {'pc2':pc2}
    #ax.add_collection(pc2)
    return subclusters3

def get_plinks(prog_links, tglist, colors, other_c='xkcd:light grey'):
    prog_links2 = {'other':{'links':[], 'cc':other_c}}
    for g in tglist:
        prog_links2[g] = {'links':[], 'cc':colors[tglist.index(g)]}
    chids = prog_links['chid'].tolist()
    xx0 = prog_links['x0'].tolist()
    yy0 = prog_links['y0'].tolist()
    xx1 = prog_links['x1'].tolist()
    yy1 = prog_links['y1'].tolist()
    ss = prog_links['no_SL'].tolist()
    for ch,x0,y0,x1,y1,s in zip(chids, xx0, yy0, xx1, yy1,ss):
        if ch in tglist:
            c = colors[tglist.index(ch)]
            link = [x0,y0,x1,y1,s,c]
            prog_links2[ch]['links'].append(link)
        else:
            c = other_c
            link = [x0,y0,x1,y1,s,c]
            prog_links2['other']['links'].append(link)
    return prog_links2

def draw_arrow(ax, link):
    x0, y0, x1, y1, s, c = link
    ax.annotate("",
        xy=(x1, y1), xycoords='data',
        xytext=(x0, y0), textcoords='data',
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        color=c,
                        lw=float(s)/50.,),
        )

def make_plot(ax, nodes):
    times = nodes['time'].tolist()
    timeset = sorted(list(set(times)))
    tcount = [ times.count(t) for t in timeset ]
    ax.plot(timeset, tcount)

def saveFigure(resultsGDF, dirpath='.', prefix='tpt_', bg_polys=[], bbox=None, vno=16, dev_scale=1.5, top_groups=5, colors=None):
    nodes = resultsGDF['nodes']
    subclusters = resultsGDF['subclusters']
    prog_links = resultsGDF['prog_links']

    if nodes['chid'].tolist()[0]=='-':
        print('no clusters found returning None')
        return None

    if not(bbox is None):
        minx, miny, maxx, maxy = bbox
    else:
        minx, miny, maxx, maxy = get_bounds(nodes, subclusters, prog_links)

    if colors is None:
        print('use sns hls color list with {} groups'.format(str(top_groups)))
        colors = sns.color_palette("hls", top_groups)

    tglist = get_top_groups(nodes, top_groups=top_groups)
    nodes2 = get_nodes(nodes, tglist, colors)
    subclusters3 = get_subcs(subclusters, tglist, colors)
    prog_links2 = get_plinks(prog_links, tglist, colors)

    fig = plt.figure(figsize=(12, 10))

    gs = gridspec.GridSpec(3,6)
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    ax2 = fig.add_subplot(gs[0:2, 2:4])
    ax3 = fig.add_subplot(gs[0:2, 4:6])
    ax4 = fig.add_subplot(gs[2, :])


    ax1.scatter(nodes2['other']['xx'], nodes2['other']['yy'], c=nodes2['other']['cc'], s=1)
    ax2.add_collection(subclusters3['other']['pc2'])
    for link in prog_links2['other']['links']:
        draw_arrow(ax3, link)
    for g in tglist:
        ax1.scatter(nodes2[g]['xx'], nodes2[g]['yy'], c=nodes2[g]['cc'], s=1)
        ax2.add_collection(subclusters3[g]['pc2'])
        for link in prog_links2[g]['links']:
            draw_arrow(ax3, link)

    for ax in [ax1,ax2,ax3]:
        ax.set_xlim([minx,maxx])
        ax.set_ylim([miny,maxy])
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

    make_plot(ax4, nodes)
    ax1.set_title('(a) point', loc='left')
    ax2.set_title('(b) subcluster', loc='left')
    ax3.set_title('(c) progression link', loc='left')
    ax4.set_title('(d) case by time', loc='left')

    plt.setp(ax4.get_xticklabels(), rotation=45)
    plt.tight_layout()
    fname = os.path.join(dirpath, prefix+'figure.png')
    plt.savefig(fname, dpi=128, bbox_inches='tight')
    return
