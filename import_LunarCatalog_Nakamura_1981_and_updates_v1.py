#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read in the Apollo catalog.

Once read in it should be saved as QuakeML format

:copyright:
    The pdart Development Team & Ceri Nunn
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import inspect
import io
import os
import warnings

from lxml import etree

from obspy.core.event import (Amplitude, Arrival, Axis, Catalog, Comment,
                              CompositeTime, ConfidenceEllipsoid, CreationInfo,
                              DataUsed, Event, EventDescription,
                              FocalMechanism, Magnitude, MomentTensor,
                              NodalPlane, NodalPlanes, Origin, OriginQuality,
                              OriginUncertainty, Pick, PrincipalAxes,
                              QuantityError, ResourceIdentifier,
                              SourceTimeFunction, StationMagnitude,
                              StationMagnitudeContribution, Tensor, TimeWindow,
                              WaveformStreamID)
from obspy.core.utcdatetime import UTCDateTime
from obspy.core.util import AttribDict

def import_apollo(file):

    '''
    Original Explanation of Catalog Entries - rev. 1008

    Columns       Data
    -------       ---------------------------------------------------------

     3 - 4        Year

     6 - 8        Day of the year

    10 - 13       Signal start time in hours and minutes

    15 - 18       Signal stop time in hours and minutes; 9999 if the signal
                  continues to the next event

    20 - 35       Signal envelope amplitudes in mm measured on a standard
                  compressed-scale plot.  Z component is used for stations
                  11 and 12, and Y component is used for all the other
                  stations.  Standard compressed plot is produced by first
                  taking the absolute value of the difference between
                  consecutive long-period data points, summing them over
                  40 data points (approx. 6 s), and then plotting them at a
                  scale of 157 digital units/cm in alternating polarities
                  to give the appearance of a seismogram.  Four columns are
                  assigned to each of Apollo stations 12 (or 11), 14, 15
                  and 16.

    37 - 40       Availability of seismograms in expanded time scale:
                    1 = Calcomp incremental plotter plot
                    2 = Versatec matrix plotter plot
                  A single column is assigned to each of stations 12
                  (or 11), 14, 15 and 16.


    42 - 45       Data quality code (single column for each station):
                    1 = no data available for the station
                    2 = noisy data
                    3 = signal is masked by another, larger event
                    4 = compressed plot is clipped (original digital data
                        may not be clipped)
                    5 = see comments
                    6 = the time recorded with the data is computer-
                        generated, and thus is not exact

    42 - 45       Data quality code (single column for each station):

    47 - 76       Comments

    77            Event type:
                    A = classified (matching) deep moonquake
                    M = unclassified deep moonquake
                    C = meteoroid impact
                    H = shallow moonquake
                    Z = mostly short-period event
                    L = LM impact
                    S = S-IVB impact
                    X = special type

    78 - 80       Matching deep moonquake class

    --- Additional entries for levent.0704 ---

    82 - 85       New deep moonquake identification, July 2004
                    A = deep moonquake with assigned number
                    T = suspected long-period thermal moonquake with assigned number
    '''

    # catalog
    catalog = Catalog()
    comment = Comment(text='Catalog based on work by Nakamura, Y., G. V. Latham, H. J. Dorman and J. E. Harris, Passive seismic experiment long-period event catalog, Final version, 1969 day 202 - 1977 day 273, 314 pp., Galveston Geophysics Laboratory, Galveston, 19 June, 1981 and Bulow, R.C., Johnson, C.L., Bills, B.G., Shearer, P.M., 2007. Temporal and spatial properties of some deep moonquake clusters. Journal of Geophysical Research 112. Compiled as a QuakeML file by Ceri Nunn, Ludwig Maximilian University, Munich.')
    catalog.comments.append(comment)
    with open(file, 'r') as af:
        for line in af:

            # read the original file
            (yr, day, sig_start_hour,
            sig_start_min, sig_end_hour, sig_end_min,
            env_11_or_12, env_14, env_15, env_16, av_11_or_12, av_14, av_15,
            av_16, qual_11_or_12, qual_14, qual_15, qual_16, comments, ev_type,
            matching_moonquake, moonquake_type, moonquake_number
            ) = (line[2:4], line[5:8], line[9:11],
            line[11:13], line[14:16], line[16:18],
            line[19:22], line[23:26], line[27:30], line[31:34], line[36],
            line[37], line[38], line[39],
            line[41], line[42], line[43],
            line[44],line[46:76], line[76], line[77:80], line[81], line[82:85])

#            print (yr, day, sig_start_hour,
#            sig_start_min, sig_end_hour, sig_end_min,
#            env_11_or_12, env_14, env_15, env_16, av_11_or_12, av_14, av_15,
#            av_16, qual_11_or_12, qual_14, qual_15, qual_16, comments, ev_type,
#            matching_moonquake, moonquake_type, moonquake_number)

            # event
            event = Event()

            # original comments
            event.comments = []
            if comments.strip() != '':
                comment = Comment(text=comments.strip())
                event.comments.append(comment)

            # overwrite the ev_type column with T if
            # thermal type is specified (from Bulow 2007)
            if moonquake_type == 'T':
                ev_type = 'T'

            # overwrite the ev_type column with A if
            # moonquake type is specified (from Bulow 2007)
            if moonquake_type == 'A':
                ev_type = 'A'

            # map the moon event types to the standard types
            if ev_type in ('A', 'M', 'H'):
                event.event_type = "earthquake"
            elif ev_type in ('C'):
                event.event_type = "meteorite"
            elif ev_type in ('L', 'S'):
                event.event_type = "crash"
            elif ev_type in ('Z', 'X', 'T'):
                event.event_type = "other event"
            elif ev_type.strip() == '':
                ev_type = 'U'
#                event.event_type = "unclassified"

            # original labels
            ev_type_label = {'A': 'classified (matching) deep moonquake',
              'M' : 'unclassified deep moonquake',
              'C' : 'meteoroid impact',
              'H' : 'shallow moonquake',
              'Z' : 'mostly short-period event',
              'L' : 'LM impact',
              'S' : 'S-IVB impact',
              'X' : 'special type',
              'T' : 'suspected thermal quake',
              'U' : 'unclassified'}

            # original quality label
            quality_label = {'1': 'no data available for the station',
                    '2' : 'noisy data',
                    '3' : 'signal is masked by another, larger event',
                    '4' : 'compressed plot is clipped (original digital data may not be clipped)',
                    '5' : 'see comments',
                    '6' : 'the time recorded with the data is computer-generated, and thus is not exact'
                        }

            # include original labels as an extra field on the event
            moon_event_extra = {
                     'moon_event_type': {'value': ev_type_label[ev_type],
                                      'namespace': r"http://some-page.de/xmlns/0.1"}}
            event.extra = moon_event_extra

            # picks
            event.picks = []

            # calculate the signal start time
            # I believe this is the signal time, and so corresponds best with
            # pick in the schema
            sig_time = UTCDateTime(year=1900+int(yr), julday=int(day),
            hour=int(sig_start_hour), minute=int(sig_start_min))

            # calculate signal duration when specified in the file
            sig_duration = None
            if sig_end_hour.strip() not in ('99', ''):
                if sig_end_hour < sig_start_hour:
                    # special case when the signal runs on to the next day
                    sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day) + 1,
                    hour=int(sig_end_hour), minute=int(sig_end_min))
                else:
                    sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day),
                    hour=int(sig_end_hour), minute=int(sig_end_min))

                sig_duration = sig_end_time - sig_time

#            if (av_11_or_12 == '1' or av_14 == '1' or av_15 == '1'
#              or av_16 == '1'):
#                print(line)
#                exit()

            # change all the envelope functions to floats
            if env_11_or_12.strip() == '':
                env_11_or_12 = None
            else:
                env_11_or_12 = float(env_11_or_12)

            if env_14.strip() == '':
                env_14 = None
            else:
                env_14 = float(env_14)

            if env_15.strip() == '':
                env_15 = None
            else:
                env_15 = float(env_15)

            if env_16.strip() == '':
                env_16 = None
            else:
                env_16 = float(env_16)

            # the file contained links to deep moonquake clusters
            # and thermal moonquake clusters.
            # Both the Nakamura paper and the Bulow paper had these
            # links. Occassionally they do not agree, so I include
            # both sets of links where they exist in the file
            extra = None
            found = False
            if matching_moonquake.strip() != '' or moonquake_number.strip() != '':
                # print(matching_moonquake.strip())
                # print('ss')
                # exit()
                if matching_moonquake.strip() == '01':
                    found = True

                if moonquake_number.strip() == '1':
                    found = True
                    # print('found')
                extra = {}
                # Nakamura link
                if matching_moonquake.strip() != '':

                    # print(matching_moonquake.strip())
                    matching_moonquake_value = '{}{}'.format(ev_type, matching_moonquake.strip())
                    extra['nakamura_moonquake'] = {'value': matching_moonquake_value,
                              'namespace': r"http://some-page.de/xmlns/1.0"}
                    comment = Comment(text='nakamura_moonquake: {}'.format(matching_moonquake_value))
                    event.comments.append(comment)
                # Bulow link
                if moonquake_number.strip() != '':
                    matching_moonquake_value = '{}{}'.format(ev_type, moonquake_number.strip())
                    extra['bulow_moonquake'] = {'value': matching_moonquake_value,
                               'namespace': r"http://some-page.de/xmlns/1.0"}
                    comment = Comment(text='bulow_moonquake: {}'.format(matching_moonquake_value))
                    event.comments.append(comment)

            # to just find the A01 cluster, use this:
            # if not found:
            #     continue

            # Now create picks at the relevant stations

            # if the data were available at 11 or 12, or the envelope is described
            # create a pick
            if av_11_or_12 in ('1','2') or env_11_or_12 is not None:
                # before this date, the station was S11
                if sig_time < UTCDateTime(year=1969, julday=239):
                    station_code='S11'
                else:
                    station_code='S12'
                pick = Pick()
                pick.time = sig_time
                pick.waveform_id = WaveformStreamID(network_code="XA",
                  station_code=station_code,location_code="", channel_code="")
                if extra is not None:
                        pick.extra = extra
                if qual_11_or_12.strip() != '':
                    comment = Comment(text=quality_label[qual_11_or_12])
                    pick.comments.append(comment)
                pick.phase_hint = 'P'
                pick.time_errors.uncertainty = 60.
                event.picks.append(pick)

                # record signal amplitude where possible
                '''
                Signal envelope amplitudes in mm measured on a standard
                compressed-scale plot.  Z component is used for stations
                11 and 12, and Y component is used for all the other
                stations.  Standard compressed plot is produced by first
                taking the absolute value of the difference between
                consecutive long-period data points, summing them over
                40 data points (approx. 6 s), and then plotting them at a
                scale of 157 digital units/cm in alternating polarities
                to give the appearance of a seismogram.  Four columns are
                assigned to each of Apollo stations 12 (or 11), 14, 15
                and 16.
                '''
                if env_11_or_12 is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = env_11_or_12
                    amplitude.type = 'A'
                    amplitude.unit = "other"
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)

                # record signal end time where possible
                if sig_duration is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = sig_duration
                    amplitude.type = 'END'
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)

            # REPEAT THE PROCESS FOR 14, 15 AND 16

            # S14
            if av_14 in ('1','2') or env_14 is not None:
                station_code='S14'
                pick = Pick()
                pick.time = sig_time
                pick.waveform_id = WaveformStreamID(network_code="XA",
                  station_code=station_code,location_code="", channel_code="")
                if extra is not None:
                    pick.extra = extra
                if qual_14.strip() != '':
                    comment = Comment(text=quality_label[qual_14])
                    pick.comments.append(comment)
                pick.phase_hint = 'P'
                pick.time_errors.uncertainty = 60.
                event.picks.append(pick)

                if env_14 is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = env_14
                    amplitude.type = 'A'
                    amplitude.unit = "other"
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)
                if sig_duration is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = sig_duration
                    amplitude.type = 'END'
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)

            #S15
            if av_15 in ('1','2') or env_15 is not None:
                station_code='S15'
                pick = Pick()
                pick.time = sig_time
                pick.waveform_id = WaveformStreamID(network_code="XA",
                  station_code=station_code,location_code="", channel_code="")
                if extra is not None:
                    pick.extra = extra
                if qual_15.strip() != '':
                    comment = Comment(text=quality_label[qual_15])
                    pick.comments.append(comment)
                pick.phase_hint = 'P'
                pick.time_errors.uncertainty = 60.
                event.picks.append(pick)

                if env_15 is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = env_15
                    amplitude.type = 'A'
                    amplitude.unit = "other"
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)
                if sig_duration is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = sig_duration
                    amplitude.type = 'END'
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)

            # S16
            if av_16 in ('1','2') or env_16 is not None:
                station_code='S16'
                pick = Pick()
                pick.time = sig_time
                pick.waveform_id = WaveformStreamID(network_code="XA",
                  station_code=station_code,location_code="", channel_code="")
                if extra is not None:
                    pick.extra = extra
                if qual_16.strip() != '':
                    comment = Comment(text=quality_label[qual_16])
                    pick.comments.append(comment)
                pick.phase_hint = 'P'
                pick.time_errors.uncertainty = 60.
                event.picks.append(pick)

                if env_16 is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = env_16
                    amplitude.type = 'A'
                    amplitude.unit = "other"
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)
                if sig_duration is not None:
                    amplitude = Amplitude()
                    amplitude.generic_amplitude = sig_duration
                    amplitude.type = 'END'
                    amplitude.pick_id = pick.resource_id
                    event.amplitudes.append(amplitude)


            # TODO start thinking about event origins
#            event.origins = []
#            origin = Origin()
#            origin.time = sig_time
#            event.origins.append(origin)
#            print (origin)


            catalog.append(event)

    # write the catalog as a validated xml file
    catalog.write("LunarCatalog_Nakamura_1981_and_updates_v1.xml", "QUAKEML",
          nsmap={"my_ns": r"http://test.org/xmlns/0.1"}, validate=True)


    print ('No of records in catalog: {}'.format(len(catalog)))


if __name__ == '__main__':
    file = 'levent.1008'
    import_apollo(file)
