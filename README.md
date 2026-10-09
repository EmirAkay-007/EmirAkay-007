<img src="assets/header.svg" width="100%" alt="Hüseyin Emir Akay. Computer Engineering student at Atatürk University; vice captain and software developer of the ARES UAV team; builds ground control stations and operator interfaces. Path so far: Atatürk University (2024), ARES ground station lead (2025), TEKNOFEST finalist 25th of 873 (2025), vice captain and finalist 34th of 1053 (2026), next: internship.">

I'm Hüseyin Emir Akay, a third-year Computer Engineering student at Atatürk University. I build ground control station and operator interface software for unmanned aerial vehicles, and I'm vice captain and software developer of the ARES UAV team, a TEKNOFEST Fighting UAV finalist in 2025 (25th of 873 teams) and 2026 (34th of 1053).

## What I work on

<img src="assets/kamikaze-dive.webp" align="right" width="300" alt="Onboard camera view of an autonomous dive in simulation: the aircraft noses down toward a target on the runway, then pulls out and climbs away.">

- **Ground control stations.** Two generations of the ARES ground control station: I built the 2025 version in C# / .NET and am a developer of the 2026 version in Python with Qt / QML. Real-time map, camera and flight data on one screen, with telemetry, video and server streams handled in parallel.
- **Guidance and autonomy.** Guidance for an autonomous dive manoeuvre (the clip shows one in simulation), QR-based target detection with recovery logic, and telemetry, geofence and waypoint handling over MAVLink. Validated in ArduPilot SITL, Gazebo and ROS 2.
- **Computer vision.** A YOLOv8 detector trained on 70,000 images, integrated into an OpenCV pipeline and running at 30–35 FPS with TensorRT.
- **Data links.** Video over a Rocket M5 radio link and JSON data exchange with the competition server.

**Currently:** an embedded target-lock system on a Raspberry Pi 4 with an AI camera and an Arduino UNO Q.

## Projects

<p>
  <a href="https://github.com/EmirAkay-007/SihaInterface"><img src="assets/card-sihainterface.svg" width="49%" alt="SihaInterface: the ARES team's ground control station, continued independently from kadir1243's original. My part: dive guidance, QR detection and flight-parameter handling. Python, PySide6, QML, pymavlink."></a>
  <a href="https://github.com/EmirAkay-007/C-_interface_mavlink"><img src="assets/card-areion.svg" width="49%" alt="ARE-İON: first-generation ground control station with live telemetry, a satellite map and onboard video in one window. C#, .NET 8, WinForms, WebView2."></a>
</p>
<p>
  <a href="https://github.com/EmirAkay-007/kampus_yolu"><img src="assets/card-kampus-yolu.svg" width="49%" alt="Kampüs Yolu: map-based campus social app with matching, chat and an admin panel. Built with a teammate; I wrote the backend. PHP, MySQL 8, JavaScript, Leaflet."></a>
  <a href="https://github.com/EmirAkay-007/dogruluk"><img src="assets/card-dogruluk.svg" width="49%" alt="Dogruluk: a linked-list-based data structure that keeps timing on the transitions between stops and produces cumulative arrival times. C++17."></a>
</p>

## Tools

- **Interfaces:** PySide6 (Qt), QML, C# / .NET (WinForms, WPF)
- **Languages:** Python, C#, C/C++, JavaScript, PHP, SQL
- **UAV and autonomy:** ArduPilot, MAVLink (pymavlink), Mission Planner, SITL, Gazebo, ROS 2
- **Vision and AI:** OpenCV, YOLOv8, PyTorch, TensorRT
- **Hardware:** Pixhawk, Jetson Orin NX, Raspberry Pi 4, Arduino UNO Q
- **Other:** Git, Linux (Ubuntu)

## Contact

[LinkedIn](https://www.linkedin.com/in/huseyinemirakay) · Open to internship opportunities in UAV operator interfaces and ground control software.

<img src="https://raw.githubusercontent.com/EmirAkay-007/EmirAkay-007/output/altitude.svg" width="100%" alt="Climb profile: cumulative GitHub contributions over the last 12 months, drawn as an altitude line that rises by one unit per contribution. Updated daily.">
