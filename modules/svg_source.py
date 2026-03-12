import math, platform

class SVG_Source:

    def svg_trashcan(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return  f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" rx="4" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(3 3)" fill-rule="evenodd" fill="{color_text}" d="M12,13.5857864 L14.2928932,11.2928932 L15.7071068,12.7071068 L13.4142136,15 L15.7071068,17.2928932 L14.2928932,18.7071068 L12,16.4142136 L9.70710678,18.7071068 L8.29289322,17.2928932 L10.5857864,15 L8.29289322,12.7071068 L9.70710678,11.2928932 L12,13.5857864 Z M7,4 L7,3 C7,1.8954305 7.8954305,1 9,1 L15,1 C16.1045695,1 17,1.8954305 17,3 L17,4 L20,4 C21.1045695,4 22,4.8954305 22,6 L22,8 C22,9.1045695 21.1045695,10 20,10 L19.9198662,10 L19,21 C19,22.1045695 18.1045695,23 17,23 L7,23 C5.8954305,23 5,22.1045695 5.00345424,21.0830455 L4.07986712,10 L4,10 C2.8954305,10 2,9.1045695 2,8 L2,6 C2,4.8954305 2.8954305,4 4,4 L7,4 Z M7,6 L4,6 L4,8 L20,8 L20,6 L17,6 L7,6 Z M6.08648886,10 L7,21 L17,21 L17.0034542,20.9169545 L17.9132005,10 L6.08648886,10 Z M15,4 L15,3 L9,3 L9,4 L15,4 Z"/>
                </svg>
                '''

    def svg_reuse(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M7.41421356,19 L9.70710678,21.2928932 L8.29289322,22.7071068 L3.58578644,18 L8.29289322,13.2928932 L9.70710678,14.7071068 L7.41421356,17 L16,17 C17.6568542,17 19,15.6568542 19,14 L19,11 L21,11 L21,14 C21,16.7614237 18.7614237,19 16,19 L7.41421356,19 Z M16.5867862,5.00099979 L14.2928932,2.70710678 L15.7071068,1.29289322 L20.4142136,6 L15.7071068,10.7071068 L14.2928932,9.29289322 L16.5847866,7.00099979 L8,7.00099979 C6.34314575,7.00099979 5,8.34414554 5,10.0009998 L5,13.0009998 L3,13.0009998 L3,10.0009998 C3,7.23957604 5.23857625,5.00099979 8,5.00099979 L16.5867862,5.00099979 Z"/>
                </svg>
                '''

    def svg_exit(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M12,23 C5.92486775,23 1,18.0751322 1,12 C1,5.92486775 5.92486775,1 12,1 C18.0751322,1 23,5.92486775 23,12 C23,18.0751322 18.0751322,23 12,23 Z M12,21 C16.9705627,21 21,16.9705627 21,12 C21,7.02943725 16.9705627,3 12,3 C7.02943725,3 3,7.02943725 3,12 C3,16.9705627 7.02943725,21 12,21 Z M12,13.4142136 L8.70710678,16.7071068 L7.29289322,15.2928932 L10.5857864,12 L7.29289322,8.70710678 L8.70710678,7.29289322 L12,10.5857864 L15.2928932,7.29289322 L16.7071068,8.70710678 L13.4142136,12 L16.7071068,15.2928932 L15.2928932,16.7071068 L12,13.4142136 Z"/>
                </svg>
                '''

    def svg_delete(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M12,12.5857864 L14.2928932,10.2928932 L15.7071068,11.7071068 L13.4142136,14 L15.7071068,16.2928932 L14.2928932,17.7071068 L12,15.4142136 L9.70710678,17.7071068 L8.29289322,16.2928932 L10.5857864,14 L8.29289322,11.7071068 L9.70710678,10.2928932 L12,12.5857864 Z M15,3.41421356 L15,7 L18.5857864,7 L15,3.41421356 Z M19,9 L15,9 C13.8954305,9 13,8.1045695 13,7 L13,3 L5,3 L5,21 L19,21 L19,9 Z M5,1 L15.4142136,1 L21,6.58578644 L21,21 C21,22.1045695 20.1045695,23 19,23 L5,23 C3.8954305,23 3,22.1045695 3,21 L3,3 C3,1.8954305 3.8954305,1 5,1 Z"/>
                </svg>
                '''

    def svg_test(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M12,12.5857864 L14.2928932,10.2928932 L15.7071068,11.7071068 L13.4142136,14 L15.7071068,16.2928932 L14.2928932,17.7071068 L12,15.4142136 L9.70710678,17.7071068 L8.29289322,16.2928932 L10.5857864,14 L8.29289322,11.7071068 L9.70710678,10.2928932 L12,12.5857864 Z M15,3.41421356 L15,7 L18.5857864,7 L15,3.41421356 Z M19,9 L15,9 C13.8954305,9 13,8.1045695 13,7 L13,3 L5,3 L5,21 L19,21 L19,9 Z M5,1 L15.4142136,1 L21,6.58578644 L21,21 C21,22.1045695 20.1045695,23 19,23 L5,23 C3.8954305,23 3,22.1045695 3,21 L3,3 C3,1.8954305 3.8954305,1 5,1 Z"/>
                </svg>
                '''

    def svg_copy(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                    <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M16,16 L16,20 C16,21.1522847 15.1522847,22 14,22 L4,22 C2.84771525,22 2,21.1522847 2,20 L2,10 C2,8.84771525 2.84771525,8 4,8 L8,8 L8,4 C8,2.84771525 8.84771525,2 10,2 L20,2 C21.1522847,2 22,2.84771525 22,4 L22,14 C22,15.1522847 21.1522847,16 20,16 L16,16 Z M14,16 L10,16 C8.84771525,16 8,15.1522847 8,14 L8,10 L4,10 L4,20 L14,20 L14,16 Z M10,4 L10,14 L20,14 L20,4 L10,4 Z"/>
                </svg>
                '''

    def svg_reset(self, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        return f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 32 32">
                <rect width="{size[0]}" height="{size[1]}" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M17.8069373,7 C16.4464601,5.07869636 14.3936238,4 12,4 C7.581722,4 4,7.581722 4,12 L2,12 C2,6.4771525 6.4771525,2 12,2 C14.8042336,2 17.274893,3.18251178 19,5.27034886 L19,2 L21,2 L21,9 L14,9 L14,7 L17.8069373,7 Z M6.19306266,17 C7.55353989,18.9213036 9.60637619,20 12,20 C16.418278,20 20,16.418278 20,12 L22,12 C22,17.5228475 17.5228475,22 12,22 C9.19576641,22 6.72510698,20.8174882 5,18.7296511 L5,22 L3,22 L3,15 L10,15 L10,17 L6.19306266,17 Z"/>
            </svg>
            '''
        
    def svg_from_text(self, symbol="?", size=(32, 32), color_background="#4a90e2", color_text="#ffffff", platform_font="Arial Bold"):
        text_size = int(math.sqrt(size[0] * size[0] + size[1] * size[1]) * (0.2 if len(symbol) > 4 else 0.25))
        text_x = size[0] // 2
        if platform.system() == "Windows":
            text_y = size[1] // 2 + text_size // 2
        else:
            text_y = size[1] // 2
        return f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}">
            <rect width="{size[0]}" height="{size[1]}" rx="{text_size//2}" ry="{text_size//2}" fill="{color_background}" stroke-width="0"/>
            <text x="{text_x}" y="{text_y}" font-family="{platform_font}" font-size="{text_size}" fill="{color_text}" stroke="none" text-anchor="middle" dominant-baseline="middle">
                {symbol}
            </text>
        </svg>'''
