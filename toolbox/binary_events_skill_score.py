## Brian Blaylock
## March 25, 2019

# Update 11 May 2021: aggregated functions into a class.

"""
=========================
Binary Event Verification
=========================

Verification of binary events with contingency table.

In data validation there are two terms that are thrown around. Let's get
these straight. 

Forecast Validation
    Detailed assessment of the forecast of a specific event.
Forecast Verification
    Assurance of the overall quality of all the forecasts.

.. note:: **Verification Resources**

    Jollliffe, I. T., D. B. Stephenson, 2012: Forecast Verification, 
        A Practitioner's Guide in Atmospheric Science. Pages 32-59.
        ISBN 13: 9780470660713.
        - Chapter 3 (Hogan and Mason) Deterministic Forecasts of binary events.
        - Tables 3.1 and 3.3
    
    http://www.wxonline.info/topics/verif2.html

    http://www.cawcr.gov.au/projects/verification/

.. note:: **Other Verification Tools**
    - `xskillscore <https://xskillscore.readthedocs.io/>`_ is a Python
    package for verification of forecsts using xarray.
    - `Model Evaluation Tools (MET) 
    <http://dtcenter.org/community-code/model-evaluation-tools-met>`_.
    is very powerful verification software developed by the
    Developmental Testbed Center (DTC).

"""

import numpy as np
import xarray as xr

class Contingency:
    """Compute skill scores for binary events.
    
    TODO:
    - What to do when array has nans or are masked arrays?
    """

    def __init__(self, observed, forecasted):
        """
        Create a contingency table for two binary fields.

        Number of hits (a), false alarms (b), misses (c), and correct 
        rejections (d).

        Parameters
        ----------
        forecasted : array_like, bool
            Array of True/False if the event was forecasted
        observed :array_like, bool
            Array of True/False if the event was observed
        """
        self.observed = observed
        self.forecasted = forecasted
               
        self._validate()
        
        self.a = self.hits
        self.b = self.false_alarms
        self.c = self.misses
        self.d = self.correct_rejections
        
        self.n_forecasted = self.a + self.b
        self.n_observed = self.a + self.c
        self.n = self.a+self.b+self.c+self.d
        
        # Other useful values
        self.a_random = (self.a+self.b)*(self.a+self.c)/self.n
        self.d_random = (self.b+self.d)*(self.c+self.d)/self.n
                
    def _validate(self):
        assert np.shape(self.observed) == np.shape(self.forecasted), "input must be the same shape"
        self.observed = self.observed.astype(bool)
        self.forecasted = self.forecasted.astype(bool)
    
    def __str__(self):
        """print the contingency table"""
        if isinstance(self.hits, xr.DataArray):
            msg = [
                '          {:^20}'.format('Observed'),
                '         │{:^10}{:^10}│ {:>10}'.format('Yes', 'No', 'Total'),
                '─────────┼────────────────────┼─────────────',
                ' Fxx Yes │{:^10,}{:^10,}│ {:>10,}'.format(self.a.item(), self.b.item(), self.a.item()+self.b.item()),
                ' Fxx No  │{:^10,}{:^10,}│ {:>10,}'.format(self.c.item(), self.d.item(), self.c.item()+self.d.item()),
                '─────────┼────────────────────┼─────────────',
                'Total    │{:^10,}{:^10,}│ {:>10,}'.format(self.a.item()+self.c.item(), self.b.item()+self.d.item(), self.n.item()),
            ]
        else:
            msg = [
                '          {:^20}'.format('Observed'),
                '         │{:^10}{:^10}│ {:>10}'.format('Yes', 'No', 'Total'),
                '─────────┼────────────────────┼─────────────',
                ' Fxx Yes │{:^10,}{:^10,}│ {:>10,}'.format(self.a, self.b, self.a+self.b),
                ' Fxx No  │{:^10,}{:^10,}│ {:>10,}'.format(self.c, self.d, self.c+self.d),
                '─────────┼────────────────────┼─────────────',
                'Total    │{:^10,}{:^10,}│ {:>10,}'.format(self.a+self.c, self.b+self.d, self.n),
            ]
        return '\n'.join(msg)
    
    @property
    def hits(self):
        """Condition is forecasted and observed (a)"""
        return np.nansum(np.logical_and(self.forecasted, self.observed))
    
    @property
    def false_alarms(self):
        """Condition is forecasted but not observed (b)"""
        return np.nansum(self.forecasted) - self.a
    
    @property
    def misses(self):
        """Condition is observed but not forecasted (c)"""
        return np.nansum(self.observed) - self.a
    
    @property
    def correct_rejections(self):
        """Condition is not forecasted and not observed (d)"""
        return np.nansum(np.logical_and(~self.forecasted, ~self.observed))
    
    def base_rate(self):
        """The probability that an event will be observed."""
        s = (self.a+self.c)/(self.n)
        return s

    def forecast_rate(self):
        """The probability that an event will forecasted."""
        r = (self.a+self.b)/(self.n)
        return r

    def frequency_bias(self):
        """
        Total events forecasted divided by the total events observed. Bias Score.
        "How did the forecast frequency of 'yes' events compare to the observed
        frequency of 'yes' events?"
        - Perfect Score: B = 1
        - Underforecast: B < 1
        - Overforcast  : B > 1
        
        Does not measure how well the forecast corresponds to the observations,
        only measures relative frequencies.
        If condition is never observed (0), then B is infinity.
        """
        B = (self.a+self.b)/(self.a+self.c)
        return B

    def hit_rate(self):
        """
        Also known as Probability of Detection (POD).
        "What fraction of the observed 'yes' events were correctly forecast?"
        - Range [0,1]; 
        - Perfect Score = 1
        
        Sensitive to hits, but ignores false alarms. Very sensitive to the
        climatological frequency of the event. Good for rare events. Can be
        artificially improved by issuing more 'yes' forecasts to increase the
        number of hits. Should be used in conjunction with the false alarm ratio.
        """
        H = self.a/(self.a+self.c)
        return H

    def probability_of_detection(self):
        """Same as hit_rate."""
        return self.hit_rate()
    
    def false_alarm_rate(self):
        """
        Also known as Probability of False Detection (POFD)
        "What fraction of the observed 'no' events were incorrectly forecast as
        'yes'?"
        - Perfect Score = 0
        
        Sensitive to false alarms, but ignores misses. Can be artificially improved
        by issuing fewer 'yes' forecasts to reduce the number of false alarms. 
        Not often reported for deterministic forecasts, but is an important 
        component of the Relative Operating Characteristic (ROC) used widely for 
        probabilistic forecasts.

        .. warning:: Do not confuse with false_alarm_ratio (FAR)
        """
        F = self.b/(self.b+self.d)
        return F

    def probability_of_false_detection(self):
        """Same as false_alarm_rate."""
        return self.false_alarm_rate()
    
    def false_alarm_ratio(self):
        """
        Often abbreviated as FAR. "What fraction of the predicted 'yes' 
        events actually did not occur (i.e., were false alarms)?"
        - Perfect Score = 0
        
        Sensitive to false alarms, but ignores misses. Very sensitive to the
        climatological frequency of the event. Should be used in conjunction with
        the hit rate. 

        .. warning:: Do not confuse with false_alarm_rate
        """
        FAR = self.b/(self.a+self.b)
        return FAR

    def success_ratio(self):
        """
        The same as 1-FAR (false alarm ratio). "What fraction of the 
        forecast 'yes' events were correctly observed?"
        - Perfect Score = 1
        
        Gives information about the likelihood of an observed event, given that it
        was forecast. It is sensitive to false alarms but ignores misses.
        """
        SR = self.a/(self.a+self.b)
        return SR

    def proportion_correct(self):
        """
        Also known as Accuracy. 
        "Overall, what fraction of the forecasts were correct?"
        - Perfect Score = 1
        - Worst case = 0
        
        """
        PC = (self.a+self.d)/(self.n)
        return PC

    def critical_success_index(self):
        """
        Also known as Threat Score (TS) or Gilbert Score (GS). 
        "How well did the forecast 'yes' events correspond to the observed 'yes'
        events?"
        - Perfect Score = 1

        The total number of correct event forecasts (hits) divided by the total
        number of event forecasts plus the number of misses. Strongly dependent
        on the base rate because it is not affected by the number of non-event
        forecasts that are not observed (correct rejections).

        Measures the fraction of observed and/or forecast events that were 
        correctly predicted. It can be thought of as the accuracy when correct 
        negatives have been removed from consideration, that is, TS is only 
        concerned with forecasts that count. Sensitive to hits, penalizes both 
        misses and false alarms. Does not distinguish source of forecast error. 
        Depends on climatological frequency of events (poorer scores for rarer 
        events) since some hits can occur purely due to random chance.
        """
        CSI = self.a/(self.a+self.b+self.c)
        return CSI

    def gilbert_skill_score(self):
        """
        Also known as the Equitable Threat Score (ETS).
        Widely used for the verification of deterministic forecasts of rare events
        such as precipitation above a large threshold. However, the score is not
        "equitable."
        "How well did the forecast 'yes' events correspond to the observed 'yes' 
        events (accounting for hits due to chance)?"
        - Range: [-1/3, 1]
        - Zero is no skill
        - Perfect Score = 1

        Measures the fraction of observed and/or forecast events that were
        correctly predicted, adjusted for hits associated with random chance
        (for example, it is easier to correctly forecast rain occurrence in a wet
        climate than in a dry climate). The ETS is often used in the verification
        of rainfall in NWP models because its "equitability" allows scores to be
        compared more fairly across different regimes. Sensitive to hits. Because
        it penalizes both misses and false alarms in the same way, it does not
        distinguish the source of forecast error.

        `a_random` is the number of hits expected a forecasts independent
        of observations (pure chance). Since (n) is in the denominator, GSS depends
        explicitly on the number of correct rejections (d). In other words, `a_r`
        is the expected (a) for a random forecast with the same forecast rate (r)
        and base rate (s).
        """
        GSS = (self.a-self.a_random)/(self.a+self.b+self.c-self.a_random)
        return GSS

    def equitable_threat_score(self):
        """Same as the gilbert skill score"""
        ETS = self.gilbert_skill_score()
        return ETS

    def heidke_skill_score(self):
        """
        Based on the proportion correct that takes into account the number of hits
        due to chance.
        "What was the accuracy of the forecast relative to that of random chance?"
        - Range [-1,1]
        - Zero is no skill
        - Perfect score = 1
        
        `a_random` is the number of hits expected a forecasts independent
        of observations (pure chance).
        `d_random` is ...
        """
        HSS = (self.a+self.d-self.a_random-self.d_random)/(self.n-self.a_random-self.d_random)
        return HSS

    def peirce_skill_score(self):
        """
        Also known as the Hanssen and Kuipers discriminant or True Skill Statistic.
        Ratio of hits to total number of events observed minus the ratio of false
        alarms to total number of non-events observed (i.e. PSS = H-F).
        "How well did the forecast separate the 'yes' events from the 'no' events?"
        - Range [-1,1]
        - Perfect Score = 1

        Uses all elements in contingency table. Does not depend on climatological 
        event frequency. The expression is identical to PSS = POD - POFD, but the 
        Peirce Skill score can also be interpreted as 
        ``(accuracy for events) + (accuracy for non-events) - 1``
                
        For rare events, PSS is unduly weighted toward the first term (same as
        POD), so this score may be more useful for more frequent events.
        """
        PSS = (self.a*self.d - self.b*self.c)/((self.b+self.d)*(self.a+self.c))
        return PSS

    def clayton_skill_score(self):
        """
        Ratio of hits to total number of events forecast minus the ratio of correct
        rejections to total number of non-events forecast.
        Analogous to the PSS except it is stratified on the forecasts rather than
        the observations.
        """
        CSS = self.a/(self.a+self.b) - self.c/(self.c+self.d)
        return CSS

    def doolittle_skill_score(self):
        """Dolittle Skill Score"""
        DSS = (self.a*self.d - self.b*self.c)/np.sqrt((self.a+self.b)(self.c+self.d)(self.a+self.c)(self.b+self.d))
        return DSS

    def log_of_odds_ratio(self):
        """Log of Odds Ratio"""
        theta = self.a*self.d/(self.b*self.c)
        LOR = np.log(theta)
        return LOR

    def odds_ratio_skill_score(self):
        """Odds Ratio Skill Score"""
        Q = (self.a*self.d-self.b*self.c)/(self.a*self.d+self.b*self.c)
        return Q

    def fractions_skill_score(self, 
                              width=None,
                              radius=None, 
                              generic_filter_kwargs={},
                              verbose=True):
        r"""
        Compute the Fractions Skill Score.
        
        As the size of the neighborhood is increased, the sharpness is 
        reduced.

        References
        ----------
        Roberts, N.M. and H.W. Lean, 2008: Scale-Selective Verification 
        of Rainfall Accumulations from High-Resolution Forecasts of 
        Convective Events. Mon. Wea. Rev., 136, 78–97, 
        https://doi.org/10.1175/2007MWR2123.1

        Parameters
        ----------
        width : int
            Width of gridpoints for the square neighborhood footprint.
            Preferably an odd number so that the width is equal in
            all directions. Used if `radius` is None.
        radius : int
            Radius of gridpoints for the circular neighborhood footprint.
            Used only if `width` is None.
        generic_filter_kwargs : dict
            By default, the generic_filter uses ``mode='constant'`` and
            ``cval=0``, which assigns points outside the domain a value
            of zero. The Roberts paper handled the edges in this way.
            You may modify this if you wish.
        """
        import scipy.ndimage as ndimage

        def fraction(values):
            """Compute the fraction of the area that is True."""
            return np.sum(values)/np.size(values)

        def radial_footprint(radius):
            """A footprint with the given radius"""
            y,x = np.ogrid[-radius: radius+1, -radius: radius+1]
            footprint = x**2+y**2 <= radius**2
            footprint = 1*footprint.astype(float)
            return footprint

        assert np.sum([width is None, radius is None]) == 1, '`width` or `radius` must be specified, but not both.'

        ################################################################
        # Generate fractions for each neighborhood
        # "These quantities assess the spatial density in the binary fields."
        #                                          - Roberts et al. 2008
        
        generic_filter_kwargs.setdefault('mode', 'constant')
        generic_filter_kwargs.setdefault('cval', 0)

        return_this = {}

        if width is not None:
            if verbose: print(f'Box footprint width: {width}x{width} grid boxes')
            return_this['method'] = ('Box Footprint', width)
            generic_filter_kwargs['size'] = width
        elif radius is not None:
            if verbose: print(f'Circular footprint radius: {radius} grid boxes')
            return_this['method'] = ('Circular Footprint', radius)
            generic_filter_kwargs['footprint'] = radial_footprint(radius)

        # NOTE: If an xarray DataSet is given, a numpy array will be returned.
        if verbose: print("Generate the fractions at each grid point.")
        obs_fracs = ndimage.generic_filter(self.observed.astype(float), fraction, **generic_filter_kwargs)
        fxx_fracs = ndimage.generic_filter(self.forecasted.astype(float), fraction, **generic_filter_kwargs)
        
        ################################################################
        # Compute the Fractions Skill Score:
        if verbose: print('Compute fractions skill score')
        MSE = np.mean((obs_fracs - fxx_fracs)**2)
        MSE_ref = np.mean(obs_fracs**2) + np.mean(fxx_fracs**2)

        FSS = 1 - (MSE/MSE_ref)

        return_this['FSS'] = FSS,
        return_this['Observed_Fraction'] = obs_fracs
        return_this['Forecasted_Fraction'] = fxx_fracs
        return_this['generic_filter_kwargs'] = generic_filter_kwargs

        return return_this
