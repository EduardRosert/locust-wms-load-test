
#!/bin/env python3
from xmltodict import OrderedDict

# WMS 1.3.0 GetCapabilities
#with open("GetCapabilities_1.3.0.xml", "r",1024, "utf-8") as stream:
#    capabilities = xmltodict.parse(stream.read())
#    layers = capabilities["WMS_Capabilities"]["Capability"]["Layer"]["Layer"]
layers = [
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'background'),
        ('Title', 'Background'), 
        ('KeywordList', None)]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'CLCH_0'), 
        ('Title', 'Cloud Cover (0 - 400 hPa) at 0'), 
        ('KeywordList', None), 
        ('Dimension',OrderedDict([
                ('@name', 'time'), 
                ('@units', 'ISO8601')])), 
        ('Extent',OrderedDict([
            ('@name', 'time'), 
            ('@default', '2019-11-07T09:00:00Z'), 
            ('@multipleValues', '0'), 
            ('@nearestValue', '0'), 
            ('#text', '2019-11-07T09:00:00Z,2019-11-09T21:00:00Z/2019-11-22T09:00:00Z/PT60H')])), 
        ('Style',OrderedDict([
            ('Name', 'default'), 
            ('Title', 'title to come'), 
            ('Abstract', 'description to come'), 
            ('LegendURL', OrderedDict([
                ('@width', ''), 
                ('@height', ''), 
                ('Format', 'image/png'), 
                ('OnlineResource', OrderedDict([
                    ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                    ('@xlink:type', 'simple'), 
                    ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=CLCH_0&style=default&width=&height=')]))]))]))]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'TMAX_2M'),
        ('Title', 'Max 2m Temperature (i)'), 
        ('KeywordList', None), 
        ('Dimension', OrderedDict([
            ('@name', 'time'), 
            ('@units', 'ISO8601')])), 
        ('Extent', OrderedDict([
            ('@name', 'time'), 
            ('@default', '2019-11-07T09:00:00Z'), 
            ('@multipleValues', '0'), 
            ('@nearestValue', '0'), 
            ('#text', '2019-11-07T09:00:00Z,2019-11-09T21:00:00Z/2019-11-22T09:00:00Z/PT60H')])), 
        ('Style', 
            [OrderedDict([
                ('Name', 'sh_all_fM80t16i4'), 
                ('Title', 'Contour shade (Range: -80 / 16)'), 
                ('Abstract', 'Method : Area fill Level range : -80 to 16 Interval : 4  Colour : All colours Used for temperature at 1, 2, and 3 hPa'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=sh_all_fM80t16i4&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'ct_red_i2_dash'), 
                ('Title', 'Contour (Interval 2, red, dash)'), 
                ('Abstract', 'Method : contour Interval : 2 Colour : Red contour contour: Dash (solid for highlight) Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=ct_red_i2_dash&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM50t58i2'), 
                ('Title', 'Additional 2 (Range: -50/58 by 2)'), 
                ('Abstract', 'Method : Area fill Level range : -80 to 56 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=sh_all_fM50t58i2&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_gry_fM72t56lst'), 
                ('Title', 'Contour shade (Range: -76 / 56)'), 
                ('Abstract', 'Method : Area fill Level range : -76 to 56 Interval : 4 Thickness : 3 Colour : Grey Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=sh_gry_fM72t56lst&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM80t56i4_v2'), 
                ('Title', 'Additional 1 (Range: -80 / 56)'), 
                ('Abstract', 'Method : Area fill Level range : -80 to 56 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=sh_all_fM80t56i4_v2&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'ct_red_i4_t3'), 
                ('Title', 'Contour (interval 4, thickness 3)'), 
                ('Abstract', 'Method : contour interval 4, thickness 3, red'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=TMAX_2M&style=ct_red_i4_t3&width=&height=')]))]))])])]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', '2t'), 
        ('Title', '2 metre temperature'), 
        ('KeywordList', None), 
        ('Dimension', OrderedDict([
            ('@name', 'time'), 
            ('@units', 'ISO8601')])), 
        ('Extent', OrderedDict([
            ('@name', 'time'), 
            ('@default', '2019-11-07T09:00:00Z'), 
            ('@multipleValues', '0'), 
            ('@nearestValue', '0'), 
            ('#text', '2019-11-07T09:00:00Z,2019-11-09T21:00:00Z/2019-11-22T09:00:00Z/PT60H')])), 
        ('Style', 
            [OrderedDict([
                ('Name', 'sh_all_fM48t56i4'), 
                ('Title', 'Contour shade (Range: -48 / 56)'), 
                ('Abstract', 'Method : Area fill Level range : -48 to 56 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM48t56i4&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM64t52i4'), 
                ('Title', 'Contour shade (Range: -64 / 52)'), 
                ('Abstract', 'Method : Area fill Level range : -64 to 52 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM64t52i4&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'ct_red_i2_dash'), 
                ('Title', 'Contour (Interval 2, red, dash)'), 
                ('Abstract', 'Method : contour Interval : 2 Colour : Red contour contour: Dash (solid for highlight) Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=ct_red_i2_dash&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM32t42i2'), 
                ('Title', 'Contour shade (Range: -32 / 42, interval 2)'), 
                ('Abstract', 'Method : Area fill Level range : -32 to 42 Interval : 2 Thickness : 3 Colour : All colours Used for temperature (850hPa)'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM32t42i2&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM48t56i4_ct_wh'), 
                ('Title', 'Contour and shade (Range: -48 / 56, interval 2)'), 
                ('Abstract', 'Method : Area fill & grey contours Level range : -48 to 56 Interval : 2 Thickness : 1 Colour : All colours Used for temperature'),
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM48t56i4_ct_wh&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM52t48i4'), 
                ('Title', 'Contour shade (Range: -52 / 48)'), 
                ('Abstract', 'Method : Area fill Level range : -52 48 Interval : 4 Thickness : 3 Colour : All colours Used for temperature (850hPa)'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM52t48i4&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM52t48i4_light'), 
                ('Title', 'Contour shade (Range: -52 / 48)'), 
                ('Abstract', 'Method : Area fill Level range : -52 to 48 Interval : 4 Thickness : 3 Colour : All colours Used for temperature (850hPa)'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM52t48i4_light&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_gry_fM72t56lst'), 
                ('Title', 'Contour shade (Range: -76 / 56)'), 
                ('Abstract', 'Method : Area fill Level range : -76 to 56 Interval : 4 Thickness : 3 Colour : Grey Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_gry_fM72t56lst&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'ct_red_i4_t3'), 
                ('Title', 'Contour (interval 4, thickness 3)'), 
                ('Abstract', 'Method : contour interval 4, thickness 3, red'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=ct_red_i4_t3&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM80t56i4_v2'), 
                ('Title', 'Additional 1 (Range: -80 / 56)'), 
                ('Abstract', 'Method : Area fill Level range : -80 to 56 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM80t56i4_v2&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'sh_all_fM50t58i2'), 
                ('Title', 'Additional 2 (Range: -50/58 by 2)'), 
                ('Abstract', 'Method : Area fill Level range : -80 to 56 Interval : 4 Thickness : 3 Colour : All colours Used for temperature'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=sh_all_fM50t58i2&width=&height=')]))]))]), 
            OrderedDict([
                ('Name', 'transparent_zero_blue'), 
                ('Title', 'Temperature below 0 C'), 
                ('Abstract', 'Method : Temperature below 0 C'), 
                ('LegendURL', OrderedDict([
                    ('@width', ''), 
                    ('@height', ''), 
                    ('Format', 'image/png'), 
                    ('OnlineResource', OrderedDict([
                        ('@xmlns:xlink', 'http://www.w3.org/1999/xlink'), 
                        ('@xlink:type', 'simple'), 
                        ('@xlink:href', 'http://example.com/wms?request=GetLegendGraphic&layer=2t&style=transparent_zero_blue&width=&height=')]))]))])])]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'foreground'), 
        ('Title', 'Foreground'), 
        ('KeywordList', None)]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'grid'), 
        ('Title', 'Grid'), 
        ('KeywordList', None)]), 
    OrderedDict([
        ('@queryable', ''), 
        ('Name', 'boundaries'), 
        ('Title', 'Boundaries'), 
        ('KeywordList', None)])
]
