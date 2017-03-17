try:
    from read_adc import read_adc
except ImportError, e:
    def read_adc(adc_num):
        return 512


