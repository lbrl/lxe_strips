#! /usr/bin/env python
# -*- coding: utf-8 -*-


# import os
import ROOT as r
import numpy as np
# import re
import sys
# import glob
import math
# import datetime as dt
# from array import array
# import subprocess as sp
# import time
# import random as rm


def main():
    r.gStyle.SetPalette( 56 )
    finname = 'hist/online.raw.v1.69062.root'
    fin = r.TFile( finname )
    t = fin.Get( 'csi' )
    #
    c1 = r.TCanvas( 'c1', 'c1', 800, 800 )
    c1.SetGrid()
    c2 = r.TCanvas( 'c2', 'c2', 800, 800 )
    c2.SetGrid()
    #
    hxy = r.TH2D( 'hxy', 'hxy', 300, -600, 600, 300, -600, 600 )
    hxy_ax, hxy_ay = hxy.GetXaxis(), hxy.GetYaxis()
    #
    hzphi = r.TH2D( 'hzphi', 'hzphi', 300, -600, 600, 300, -4, 4 )
    hzphi_ax, hzphi_ay = hzphi.GetXaxis(), hzphi.GetYaxis()
    #
    ell = r.TEllipse()
    ell.SetFillStyle( 0 )
    ell.SetLineStyle( 1 )
    ell.SetLineWidth( 1 )
    ell.SetLineColor( r.kBlue )
    lat = r.TLatex()
    lat.SetTextFont( 12 )
    lat.SetTextSize( .02 )
    lat.SetTextAlign( 22 )
    #
    for eve in t:
        if eve.numer_cross > 2000:
            continue
        if eve.ntower < 1:
            continue
        tow_en_tot = 0.
        for i in xrange( eve.ntower ):
            tow_en_tot += eve.tower_energy[i]
        if tow_en_tot < 150:
            continue
        hxy.Reset()
        hzphi.Reset()
        for i in xrange( eve.numer_cross ):
            bin_x = hxy_ax.FindBin( eve.X_cross[i] )
            bin_y = hxy_ay.FindBin( eve.Y_cross[i] )
            hxy.SetBinContent( bin_x, bin_y, 1. )
            #
            phi = math.atan2( eve.X_cross[i], eve.Y_cross[i] )
            bin_phi = hzphi_ay.FindBin( phi )
            bin_z = hzphi_ax.FindBin( eve.Z_cross[i] )
            hzphi.SetBinContent( bin_z, bin_phi, hzphi.GetBinContent(bin_z, bin_phi) + 1. )
        #
        c1.cd()
        hxy.Draw( 'colz' )
        for i in xrange( eve.ntower ):
            ell.DrawEllipse( 500.*math.cos(eve.tower_phi[i]), 500.*math.sin(eve.tower_phi[i]), 25, 25, 0, 360, 0 )
            lat.DrawLatex( 500.*math.cos(eve.tower_phi[i]), 500.*math.sin(eve.tower_phi[i]), '{:.1f}'.format( eve.tower_energy[i] ) )
        c1.Update()
        #
        c2.cd()
        hzphi.Draw( 'colz' )
        for i in xrange( eve.ntower ):
            ell.DrawEllipse( 500./math.tan(eve.tower_theta[i]), eve.tower_phi[i]-math.pi, 25, .2, 0, 360, 0 )
            lat.DrawLatex( 500./math.tan(eve.tower_theta[i]), eve.tower_phi[i]-math.pi, '{:.1f}'.format( eve.tower_energy[i] ) )
        c2.Update()
        #
        raw_input()


if __name__ == '__main__':
    main()
