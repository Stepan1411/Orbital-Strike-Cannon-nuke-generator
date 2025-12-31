import math
import sys

def generate_centered_layers(layer_tnts, min_strength, max_strength, vertical_boost, fuse, spawn_height=0):
    commands = []
    num_layers = len(layer_tnts)
    
    for layer in range(num_layers):
        tnts_this_layer = layer_tnts[layer]
        
        # slightly gentler outward acceleration curve
        if num_layers > 1:
            strength = round(min_strength + (max_strength - min_strength) * ((layer / (num_layers - 1)) ** 0.95), 3)
        else:
            strength = min_strength
        
        # small vertical taper for smoother motion
        my = round(vertical_boost + (layer * 0.022), 3)
        
        for i in range(tnts_this_layer):
            angle = (2 * math.pi / tnts_this_layer) * i
            mx = round(math.cos(angle) * strength, 3)
            mz = round(math.sin(angle) * strength, 3)
            commands.append(f"summon tnt ~ ~{spawn_height} ~ {{Motion:[{mx},{my},{mz}],fuse:{fuse}}}")
    
    return commands

def generate_layer_tnts(num_layers, start_tnts=31, increment=7):
    layer_tnts = []
    for i in range(num_layers):
        layer_tnts.append(start_tnts + (i * increment))
    return layer_tnts

if __name__ == "__main__":
    print("=== TNT Sphere Generator ===\n")
    
    try:
        num_layers = int(input("Number of TNT circles: "))
        
        use_custom = input("Customize TNT count in circles? (y/n, default=n): ").strip().lower()
        
        if use_custom == 'y':
            start_input = input("TNT count in first circle (default=31): ").strip()
            start_tnts = int(start_input) if start_input else 31
            
            inc_input = input("TNT increment per circle (default=7): ").strip()
            increment = int(inc_input) if inc_input else 7
            
            layer_tnts = generate_layer_tnts(num_layers, start_tnts, increment)
        else:
            layer_tnts = generate_layer_tnts(num_layers)
        
        print(f"\nTNT count per circle: {layer_tnts}")
        print(f"Total TNT: {sum(layer_tnts)}\n")
        
        height_input = input("Spawn height offset (e.g., 0, 1.5, -2, default=0): ").strip()
        spawn_height = float(height_input) if height_input else 0
        
        min_strength = float(input("Outward speed (inner circle): "))
        max_strength = float(input("Outward speed (outer circle): "))
        vertical_boost = float(input("Vertical boost: "))
        
        fuse_input = input("Fuse time in ticks (default=80): ").strip()
        fuse = int(fuse_input) if fuse_input else 80
        
        out = generate_centered_layers(layer_tnts, min_strength, max_strength, vertical_boost, fuse, spawn_height)
        
        print(f"\n=== Generated {len(out)} commands ===\n")
        
        save_file = input("Save to file? (y/n): ").strip().lower()
        
        if save_file == 'y':
            filename = input("Filename (default=tnt_commands.txt): ").strip() or "tnt_commands.txt"
            
            # Ensure .txt extension
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            with open(filename, 'w') as f:
                for cmd in out:
                    f.write(cmd + '\n')
            
            print(f"\nCommands saved to {filename}")
            print("Press Enter to exit...")
            input()
        else:
            print("\nExiting without saving...")
            sys.exit(0)
                
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
