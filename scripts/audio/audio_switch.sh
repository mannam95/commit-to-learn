#!/bin/bash

# Audio Switch Script
# Switches both speaker (sink) and microphone (source) to the same audio device

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if pactl is available
if ! command -v pactl &> /dev/null; then
    error "pactl not found. Please install PulseAudio or PipeWire."
    exit 1
fi

# Get all sinks (speakers/headphones) - filter out virtual/monitor sinks
get_sinks() {
    pactl list sinks | awk '
        /Name:/ { name = $2 }
        /Description:/ {
            desc = substr($0, index($0, ":") + 2)
            # Skip virtual/null sinks
            if (name !~ /null|auto_null|Loopback/) {
                print name "|" desc
            }
        }
    '
}

# Get all sources (microphones) - filter out monitor sources
get_sources() {
    pactl list sources | awk '
        /Name:/ { name = $2 }
        /Description:/ {
            desc = substr($0, index($0, ":") + 2)
            # Skip monitor sources (they capture system audio, not microphone)
            if (name !~ /\.monitor$/ && name !~ /null|auto_null|Loopback/) {
                print name "|" desc
            }
        }
    '
}

# Find matching sink and source for a device
# Tries to match by common identifier (e.g., "Jabra", "HDA Intel", etc.)
find_device_pair() {
    local pattern="$1"
    local sink_name=""
    local source_name=""

    # Find matching sink
    sink_name=$(get_sinks | grep -i "$pattern" | head -1 | cut -d'|' -f1)

    # Find matching source
    source_name=$(get_sources | grep -i "$pattern" | head -1 | cut -d'|' -f1)

    echo "${sink_name}|${source_name}"
}

# Move all active audio streams to the new sink
move_sink_inputs() {
    local new_sink="$1"
    pactl list short sink-inputs 2>/dev/null | while read -r index _; do
        pactl move-sink-input "$index" "$new_sink" 2>/dev/null || true
    done
}

# Move all active recording streams to the new source
move_source_outputs() {
    local new_source="$1"
    pactl list short source-outputs 2>/dev/null | while read -r index _; do
        pactl move-source-output "$index" "$new_source" 2>/dev/null || true
    done
}

# Set default sink and source, and move existing streams
set_audio_device() {
    local sink_name="$1"
    local source_name="$2"
    local device_label="$3"

    if [ -z "$sink_name" ]; then
        error "No speaker/output found for $device_label"
        return 1
    fi

    if [ -z "$source_name" ]; then
        warn "No microphone/input found for $device_label (speaker only)"
    fi

    # Set default sink (speaker)
    info "Setting speaker to: $sink_name"
    if ! pactl set-default-sink "$sink_name"; then
        error "Failed to set default speaker"
        return 1
    fi

    # Move existing playback streams
    move_sink_inputs "$sink_name"

    # Set default source (microphone) if available
    if [ -n "$source_name" ]; then
        info "Setting microphone to: $source_name"
        if ! pactl set-default-source "$source_name"; then
            warn "Failed to set default microphone"
        else
            move_source_outputs "$source_name"
        fi
    fi

    # Small delay to let PulseAudio/PipeWire process changes
    sleep 0.3

    # Verify the switch
    verify_switch "$sink_name" "$source_name"
}

# Verify the audio device was switched correctly
verify_switch() {
    local expected_sink="$1"
    local expected_source="$2"

    local current_sink=$(pactl get-default-sink 2>/dev/null)
    local current_source=$(pactl get-default-source 2>/dev/null)

    echo ""
    if [ "$current_sink" = "$expected_sink" ]; then
        info "Speaker switched successfully"
    else
        warn "Speaker may not have switched correctly"
        warn "  Expected: $expected_sink"
        warn "  Current:  $current_sink"
    fi

    if [ -n "$expected_source" ]; then
        if [ "$current_source" = "$expected_source" ]; then
            info "Microphone switched successfully"
        else
            warn "Microphone may not have switched correctly"
            warn "  Expected: $expected_source"
            warn "  Current:  $current_source"
        fi
    fi
}

# Build dynamic menu from available devices
build_device_menu() {
    local -a devices=()
    local -a patterns=()
    local index=1

    echo -e "${CYAN}Available Audio Devices:${NC}"
    echo ""

    # Get unique device identifiers from sinks
    while IFS='|' read -r name desc; do
        [ -z "$name" ] && continue

        # Extract a meaningful pattern from the description
        local pattern=""
        local label=""

        if echo "$desc" | grep -qi "jabra"; then
            pattern="jabra"
            label="$desc"
        elif echo "$desc" | grep -qi "usb"; then
            # Generic USB audio
            pattern=$(echo "$name" | sed 's/.*\(usb[^.]*\).*/\1/i' | head -c 20)
            label="$desc"
        elif echo "$desc" | grep -qi "hdmi\|displayport"; then
            pattern="hdmi"
            label="$desc (HDMI/DisplayPort)"
        elif echo "$desc" | grep -qi "built-in\|internal\|analog\|hda intel\|generic"; then
            pattern="Generic\|Analog\|HDA"
            label="Built-in Audio ($desc)"
        elif echo "$desc" | grep -qi "bluetooth\|a2dp\|hsp\|hfp"; then
            pattern="bluetooth\|bluez"
            label="$desc (Bluetooth)"
        else
            pattern="$name"
            label="$desc"
        fi

        # Check if we already have this pattern
        local found=0
        for p in "${patterns[@]}"; do
            if [ "$p" = "$pattern" ]; then
                found=1
                break
            fi
        done

        if [ $found -eq 0 ] && [ -n "$pattern" ]; then
            patterns+=("$pattern")
            devices+=("$label")
            echo -e "  ${GREEN}$index.${NC} $label"
            ((index++))
        fi
    done < <(get_sinks)

    echo ""
    echo -e "  ${GREEN}l.${NC} List all raw devices (debug)"
    echo -e "  ${GREEN}q.${NC} Quit"
    echo ""

    # Export for use in main
    MENU_PATTERNS=("${patterns[@]}")
    MENU_DEVICES=("${devices[@]}")
}

# List raw devices for debugging
list_raw_devices() {
    echo ""
    echo -e "${CYAN}=== Speakers (Sinks) ===${NC}"
    get_sinks | while IFS='|' read -r name desc; do
        echo "  $name"
        echo "    -> $desc"
    done

    echo ""
    echo -e "${CYAN}=== Microphones (Sources) ===${NC}"
    get_sources | while IFS='|' read -r name desc; do
        echo "  $name"
        echo "    -> $desc"
    done
    echo ""
}

# Show current audio devices
show_current() {
    local current_sink=$(pactl get-default-sink 2>/dev/null)
    local current_source=$(pactl get-default-source 2>/dev/null)

    echo -e "${CYAN}Current Audio Devices:${NC}"
    echo -e "  Speaker:    $current_sink"
    echo -e "  Microphone: $current_source"
    echo ""
}

# Main
main() {
    show_current
    build_device_menu

    read -p "Enter your choice: " choice

    case "$choice" in
        [0-9]|[0-9][0-9])
            local idx=$((choice - 1))
            if [ $idx -ge 0 ] && [ $idx -lt ${#MENU_PATTERNS[@]} ]; then
                local pattern="${MENU_PATTERNS[$idx]}"
                local label="${MENU_DEVICES[$idx]}"

                info "Switching to: $label"

                IFS='|' read -r sink_name source_name <<< "$(find_device_pair "$pattern")"
                set_audio_device "$sink_name" "$source_name" "$label"
            else
                error "Invalid choice: $choice"
                exit 1
            fi
            ;;
        l|L)
            list_raw_devices
            ;;
        q|Q)
            info "Exiting"
            exit 0
            ;;
        *)
            error "Invalid choice: $choice"
            exit 1
            ;;
    esac
}

main
