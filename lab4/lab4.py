import os
import sys

os.environ['TCL_LIBRARY'] = os.path.join(sys.base_prefix, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(sys.base_prefix, 'tcl', 'tk8.6')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

t = np.linspace(0, 10, 1000)
fs = 1 / (t[1] - t[0])

class SignalState:
    def __init__(self):
        self.amp = 0.97
        self.freq = 0.267
        self.phase = 0.000
        self.noise_mean = 0.108
        self.noise_cov = 0.05
        self.cutoff = 3.0
        self.show_noise = True
        self.noise = np.random.normal(self.noise_mean, np.sqrt(self.noise_cov), len(t))

    def update_noise(self, mean, cov):
        if mean != self.noise_mean or cov != self.noise_cov:
            self.noise = np.random.normal(mean, np.sqrt(cov), len(t))
            self.noise_mean = mean
            self.noise_cov = cov
        return self.noise

state = SignalState()

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    clean_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise_signal = state.update_noise(noise_mean, noise_covariance)
    if show_noise:
        return clean_signal + noise_signal, clean_signal
    else:
        return clean_signal, clean_signal

def lowpass_filter(data, cutoff_freq, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff_freq / nyq
    if normal_cutoff >= 1.0: normal_cutoff = 0.99
    if normal_cutoff <= 0.0: normal_cutoff = 0.01
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(11, 8.5), facecolor='#121214')
ax.set_facecolor('#1a1a1e')
plt.subplots_adjust(left=0.1, bottom=0.42, right=0.9, top=0.93)

noisy, clean = harmonic_with_noise(state.amp, state.freq, state.phase, state.noise_mean, state.noise_cov, state.show_noise)
filtered = lowpass_filter(noisy, state.cutoff, fs)

line_noisy, = ax.plot(t, noisy, color='#ff9f43', alpha=0.6, linewidth=1, label='Noisy Signal')
line_clean, = ax.plot(t, clean, color='#00d2d3', linestyle='--', linewidth=2.5, label='Clean Harmonic')
line_filtered, = ax.plot(t, filtered, color='#1dd1a1', linewidth=2.5, label='Filtered Signal')

ax.set_ylim(-2.5, 2.5)
ax.set_xlim(0, 10)
ax.grid(True, color='#2d2d30', linestyle=':', linewidth=0.8)
ax.set_title("Harmonic Signal Processing Dashboard", fontsize=14, fontweight='bold', color='#f5f5f7', pad=15)
ax.legend(loc='upper right', facecolor='#1a1a1e', edgecolor='#2d2d30', labelcolor='#f5f5f7')

widget_bg = '#1a1a1e'
slider_color = '#00d2d3'

ax_amp = plt.axes([0.22, 0.34, 0.6, 0.025], facecolor=widget_bg)
ax_freq = plt.axes([0.22, 0.29, 0.6, 0.025], facecolor=widget_bg)
ax_phase = plt.axes([0.22, 0.24, 0.6, 0.025], facecolor=widget_bg)
ax_mean = plt.axes([0.22, 0.19, 0.6, 0.025], facecolor=widget_bg)
ax_cov = plt.axes([0.22, 0.14, 0.6, 0.025], facecolor=widget_bg)
ax_cut = plt.axes([0.22, 0.09, 0.6, 0.025], facecolor=widget_bg)

s_amp = Slider(ax_amp, 'Amplitude', 0.1, 2.0, valinit=state.amp, valfmt='%0.2f', color=slider_color)
s_freq = Slider(ax_freq, 'Frequency', 0.05, 1.5, valinit=state.freq, valfmt='%0.3f', color=slider_color)
s_phase = Slider(ax_phase, 'Phase', -np.pi, np.pi, valinit=state.phase, valfmt='%0.3f', color=slider_color)
s_mean = Slider(ax_mean, 'Noise Mean', -0.5, 0.5, valinit=state.noise_mean, valfmt='%0.3f', color='#ff9f43')
s_cov = Slider(ax_cov, 'Noise Variance', 0.001, 0.3, valinit=state.noise_cov, valfmt='%0.3f', color='#ff9f43')
s_cut = Slider(ax_cut, 'Filter Cutoff', 0.5, 15.0, valinit=state.cutoff, valfmt='%0.1f', color='#1dd1a1')

for s in [s_amp, s_freq, s_phase, s_mean, s_cov, s_cut]:
    s.label.set_color('#f5f5f7')
    s.label.set_fontsize(10)
    s.valtext.set_color('#f5f5f7')

ax_check = plt.axes([0.72, 0.02, 0.15, 0.04], facecolor=widget_bg)
check = CheckButtons(ax_check, ['Show Noise'], [state.show_noise])
check.labels[0].set_color('#f5f5f7')

ax_reset = plt.axes([0.15, 0.02, 0.12, 0.04], facecolor=widget_bg)
btn_reset = Button(ax_reset, 'Reset Dashboard', color='#2d2d30', hovercolor='#ff4757')
btn_reset.label.set_color('#f5f5f7')
btn_reset.label.set_fontsize(10)

def update(val):
    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    mean = s_mean.val
    cov = s_cov.val
    cutoff = s_cut.val
    show_noise = check.get_status()[0]

    noisy_data, clean_data = harmonic_with_noise(amp, freq, phase, mean, cov, show_noise)
    filtered_data = lowpass_filter(noisy_data, cutoff, fs)

    line_clean.set_ydata(clean_data)
    line_filtered.set_ydata(filtered_data)

    if show_noise:
        line_noisy.set_ydata(noisy_data)
        line_noisy.set_visible(True)
    else:
        line_noisy.set_visible(False)

    fig.canvas.draw_idle()

s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_mean.on_changed(update)
s_cov.on_changed(update)
s_cut.on_changed(update)
check.on_clicked(update)

def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_mean.reset()
    s_cov.reset()
    s_cut.reset()
    if not check.get_status()[0]:
        check.set_active(0)
    update(None)

btn_reset.on_clicked(reset)

plt.show()