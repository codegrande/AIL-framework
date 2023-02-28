#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import sys

from flask import url_for
from pymisp import MISPObject

sys.path.append(os.environ['AIL_BIN'])
##################################
# Import Project packages
##################################
from lib.ConfigLoader import ConfigLoader
from lib.objects.abstract_subtype_object import AbstractSubtypeObject, get_all_id

config_loader = ConfigLoader()
baseurl = config_loader.get_config_str("Notifications", "ail_domain")
config_loader = None


################################################################################
################################################################################
################################################################################

class Pgp(AbstractSubtypeObject):
    """
    AIL Pgp Object. (strings)
    """

    def __init__(self, id, subtype):
        super(Pgp, self).__init__('pgp', id, subtype=subtype)

    # def get_ail_2_ail_payload(self):
    #     payload = {'raw': self.get_gzip_content(b64=True),
    #                 'compress': 'gzip'}
    #     return payload

    # # WARNING: UNCLEAN DELETE /!\ TEST ONLY /!\
    def delete(self):
        # # TODO:
        pass

    # # TODO: 
    def get_meta(self, options=set()):
        meta = self._get_meta(options=options)
        meta['id'] = self.id
        meta['subtype'] = self.subtype
        meta['tags'] = self.get_tags(r_list=True)
        return meta

    def get_link(self, flask_context=False):
        if flask_context:
            url = url_for('correlation.show_correlation', type=self.type, subtype=self.subtype, id=self.id)
        else:
            url = f'{baseurl}/correlation/show?type={self.type}&subtype={self.subtype}&id={self.id}'
        return url

    def get_svg_icon(self):
        if self.subtype == 'key':
            icon = '\uf084'
        elif self.subtype == 'name':
            icon = '\uf507'
        elif self.subtype == 'mail':
            icon = '\uf1fa'
        else:
            icon = 'times'
        return {'style': 'fas', 'icon': icon, 'color': '#44AA99', 'radius': 5}

    def get_misp_object(self):
        obj_attrs = []
        obj = MISPObject('pgp-meta')
        obj.first_seen = self.get_first_seen()
        obj.last_seen = self.get_last_seen()

        if self.subtype == 'key':
            obj_attrs.append(obj.add_attribute('key-id', value=self.id))
        elif self.subtype == 'name':
            obj_attrs.append(obj.add_attribute('user-id-name', value=self.id))
        else:  # mail
            obj_attrs.append(obj.add_attribute('user-id-email', value=self.id))

        for obj_attr in obj_attrs:
            for tag in self.get_tags():
                obj_attr.add_tag(tag)
        return obj

    ############################################################################
    ############################################################################

def get_all_subtypes():
    return ['key', 'mail', 'name']

def get_all_pgps():
    pgps = {}
    for subtype in get_all_subtypes():
        pgps[subtype] = get_all_pgps_by_subtype(subtype)
    return pgps

def get_all_pgps_by_subtype(subtype):
    return get_all_id('pgp', subtype)


# if __name__ == '__main__':
