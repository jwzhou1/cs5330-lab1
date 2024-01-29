## How to Open and Use the Project

1. Open your terminal.
2. Enter the following command:
   ```
   python lab1.py
   ```
3. Open local URL in terminal to start the project in Gradio.
4. Drag and drop an image into the left box.
5. The right box will display the generated image with identified sky regions.
6. In the generated image from 'lab1,' non-sky elements are covered with black pixels, while the sky remains visible without black pixel overlay.
7. For a visual demonstration, refer to the `Demo.md` file.

--- 


**Disclaimer (Limitation):**

- The algorithm may encounter limitations in accurately identifying sky regions in images with irregularly shaped architectural structures.
- Reflections on building surfaces might pose challenges for the algorithm, impacting its ability to distinguish the sky accurately.
- Instances where buildings have protruding elements such as poles may lead to difficulties in sky segmentation.
- The algorithm may face challenges in distinguishing between sky and water bodies, especially when lakes or bodies of water seamlessly blend with the sky due to similar color tones.
- Partial occlusion of the sky, whether by buildings or other objects, may compromise the accuracy of the segmentation process.
- The algorithm may struggle to differentiate between sky and extensive white cloud cover, potentially affecting the precision of the segmentation results.