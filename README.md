┌───────────────────────────────────────────────────────┐
│          Advanced Color Adjust (HDR+Channels)         │
├───────────┬─────────────────────────────────────────┤
│  Image    │                                         │
├───────────┘                                         │
│                                                     │
│  Brightness: [1.00 ──────○─────────────] 3.00       │
│  Contrast:   [1.00 ────○───────────────] 3.00       │
│  HDR Intensity: [0.00 ─○───────────────] 1.00       │
│                                                     │
│  Channel Adjustments:                               │
│    Red:   [1.00 ───○─────────────────] 2.00         │
│    Green: [1.00 ─────○───────────────] 2.00         │
│    Blue:  [1.00 ─○───────────────────] 2.00         │
│                                                     │
├───────────┬─────────────────────────────────────────┤
│  Mask     │ (optional)                             │
├───────────┼─────────────────────────────────────────┤
│  HDR Mask │ (optional)                             │
└───────────┴─────────────────────────────────────────┘
This custom ComfyUI node allows for advanced image processing with mask support, brightness/contrast control, and optional HDR effects.
Inputs:

    Image – Input image to be processed.

    Main Mask (optional) – Mask that applies to all adjustments (e.g., brightness, contrast).

    HDR Mask (optional)

Main Parameters:

    Brightness – slider from 0.0 to 3.0 (default: 1.0)

    Contrast – slider from 0.0 to 3.0 (default: 1.0)

    HDR Intensity – slider from 0.0 to 1.0 (default: 0.0)

Channel Settings:

    Red – separate slider for the red channel

    Green – separate slider for the green channel

    Blue – separate slider for the blue channel
    (All range from 0.0 to 2.0, default: 1.0)

Bottom Section:

    Optional input for the main mask (applies to all adjustments)

    Optional input for the HDR mask (only affects the HDR effect)



Основные параметры:

    Brightness - слайдер от 0.0 до 3.0 (по умолчанию 1.0)

    Contrast - слайдер от 0.0 до 3.0 (по умолчанию 1.0)

    HDR Intensity - слайдер от 0.0 до 1.0 (по умолчанию 0.0)

Настройки каналов:

    Red - отдельный слайдер для красного канала

    Green - отдельный слайдер для зеленого канала

    Blue - отдельный слайдер для синего канала
    (Все от 0.0 до 2.0, по умолчанию 1.0)

Нижняя часть:

    Необязательный вход для основной маски (применяется ко всем корректировкам)

    Необязательный вход для HDR-маски (только для HDR-эффекта)
