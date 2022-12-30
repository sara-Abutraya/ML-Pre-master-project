import pickle;
import numpy as np

__model = None
__scalerobj= None


def predict_price(address, rooms, bathrooms, area, floor, age, finishing, view):
    col_ls = ['rooms', 'bathrooms', 'area', 'floor', 'age', 'finishing_Lux',
       'finishing_extra_super_lux', 'finishing_semi_finished',
       'finishing_super_lux', 'finishing_without_finish', 'view_Corner',
       'view_Garden', 'view_main_street', 'view_side_street',
       'view_waterview', 'zone_10th_of_radman_qarPropetries',
       'zone_arayat_el_maadi', 'zone_cairo_hdyq_lhrmqarPropetries',
       'zone_el_maadi_el_gededa', 'zone_el_salam_qarPropetries',
       'zone_el_sayyeda_zeinab_qarPropetries', 'zone_heliopolis',
       'zone_helwan-gardens', 'zone_helwan_helwan',
       'zone_houbra_elkhalafwai', 'zone_kwrnysh-helwan_helwan',
       'zone_maadi_compounds', 'zone_marga_qarPropetries',
       'zone_matarya_qarPropetries', 'zone_mokattam_qarPropetries',
       'zone_nasr-city', 'zone_new-administrative-capital',
       'zone_new-heliopolis', 'zone_oubour', 'zone_saqr_quraishMaadi',
       'zone_shorouk', 'zone_shoubra_elsahel', 'zone_shoubra_jzyr',
       'zone_shoubra_rod_elfarag', 'zone_tagamo3', 'zone_zahraa_el_maadi']
    x = np.zeros(len(col_ls))
    ## View
    view_index = col_ls.index(view)
    ## finishing
    finishing_index = col_ls.index(finishing)
    ## location
    address_index = col_ls.index(address)


    x[0] = rooms
    x[1] = bathrooms
    x[2] = area
    x[3] = floor
    x[4] = age

    if address_index >= 0:
        x[address_index] = 1

    if finishing_index >= 0:
        x[finishing_index] = 1

    if view_index >= 0:
        x[view_index] = 1

    # load scaler
    scaleredX = __scalerobj.transform([x])
    return np.around(np.exp(__model.predict(scaleredX)[0]),3)


def load_saved_objects():
    global __model
    global __scalerobj
    if __model is None:
        with open('model/RF_model.pickle', 'rb') as f:
            __model = pickle.load(f)

    if __scalerobj is None:
        with open('model/scaler.pickle', 'rb') as f:
            __scalerobj = pickle.load(f)