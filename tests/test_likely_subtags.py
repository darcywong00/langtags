#!/usr/bin/python

import unittest, os, re
from xml.etree import ElementTree as et
from palaso.sldr.langtags_full import LangTags, LangTag

def isnotint(s):
    try:
        x = int(s)
        return False
    except ValueError:
        return True

langtagtxt = os.path.join(os.path.dirname(__file__), '..', 'pub', 'langtags.txt')
exceptions = ['ji-Hebr-UA', 'kxc-Ethi', 'bji-Ethi']

class LikelySubtags(unittest.TestCase):
    ''' Tests alltags.txt for discrepencies against likelySubtags.xml '''
    def setUp(self):
        self.likelymap = {}
        thisdir = os.path.dirname(__file__)
        self.ltags = LangTags(alltags=langtagtxt)
        doc = et.parse(os.path.join(thisdir, "likelySubtags.xml"))
        for e in doc.findall("./likelySubtags/likelySubtag"):
            tolt = LangTag(e.get('to').replace("_", "-"))
            if tolt.region == "ZZ":
                tolt.hideregion = True
            if tolt.script == "Zyyy":
                tolt.hidescript = True
            self.likelymap[e.get('from').replace("_", "-")] = tolt

    def test_noBadMappings(self):
        for k, v in self.likelymap.items():
            t = LangTag(k)
            r = str(v)
            if r in exceptions:
                continue
            if t.lang=="und" or t.region=="ZZ" or t.script=="Zyyy":
                continue
            if k in self.ltags:
                if r not in self.ltags:
                    self.fail(r + " is missing from langtags")
                self.assertIs(self.ltags[k], self.ltags[r])

    def test_noBadComponents(self):
        for v in self.ltags.values():
            if v.lang is None:
                self.fail(repr(v) + " has no language")
            if len(v.lang) > 3 and "-" not in v.lang:
                self.fail(repr(v) + " has odd lang length")
            if v.region is not None and len(v.region) > 2 and isnotint(v.region):
                self.fail(repr(v) + " has bad region")

    def test_zh_CN(self):
        lt = self.ltags['zh']
        self.assertEqual(str(lt), 'zh-CN')

    def test_noDuplicates(self):
        found = {}
        with open(langtagtxt) as inf:
            for i, l in enumerate(inf.readlines()):
                for t in (x.replace("*", "") for x in re.split(r'\s*=\s*', l.strip())):
                    if t in found and found[t] != i + 1:
                        self.fail("Duplicate of {} found at lines {} and {}".format(t, found[t], i+1))
                    found[t] = i + 1
            

if __name__ == '__main__':
    unittest.main()
