
class EEGSystemNames(object):
    """
    These are string flags for the EEG systems.
    This is intended to be used to specify the specific eeg data collection system at work.

    for example:

    import CCDLUtil.Utility.Constants as CCDLConstants

    if eeg_system == CCDLConstants.EEGSystemNames.BRAIN_AMP:
        // <brain amp code>
    elif eeg_system == CCDLConstants.EEGSystemNames.GUSB_AMP:
        // <gusb amp code>
    etc.
    """
    BRAIN_AMP = 'brain_amp'
    GUSB_AMP = 'g_usb_amp'
    OpenBCI = 'open_bci'
    EMOTIV = 'emotiv'
    ALL_NAMES = {BRAIN_AMP, GUSB_AMP, OpenBCI, EMOTIV}
