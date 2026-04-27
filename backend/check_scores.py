from app.analysis.image.copy_move import analyze_copy_move
from app.analysis.ai.detector import analyze_ai_edited_image

case_id = "CASE-20260327-HVTTC6"
forged_path = "uploads/CASE-20260327-HVTTC6/WhatsApp Image 2026-03-25 at 9.52.44 PM-d53c44eb.jpeg"
authentic_path = "uploads/CASE-20260327-HVTTC6/WhatsApp Image 2026-03-27 at 11.10.20 AM-c4fce4b4.jpeg"

for label, image_path in [("FORGED", forged_path), ("AUTHENTIC", authentic_path)]:
    print(f"\n======== {label} ========")
    try:
        ai_res = analyze_ai_edited_image(case_id, image_path)
        print("AI Score:", ai_res["confidence_score"])
        print("AI ELA Score:", ai_res["findings"]["ela_score"])
        print("AI Edge Ratio:", ai_res["findings"]["edge_ratio"])
        print("AI Noise Vari:", ai_res["findings"]["noise_inconsistency"])
        print("AI Comp Score:", ai_res["findings"]["compression_artifact_score"])
    except Exception as e:
        print("Error:", e)
