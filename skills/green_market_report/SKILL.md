---
name: green_market_report
description: This skill should be used when users need to generate a structured PDF reflection report for the "Green Life Circular Market" activity, integrating text data, image captions, and file size validation.
---

# Green Market Report Generator

This skill automates the creation of a professional PDF reflection report by collecting activity metadata, process details, challenges, and image-caption pairs.

## Workflow

### Phase 1: Data Collection
1.  **Collect Student Metadata**: Prompt the user to provide `class`, `student_id`, `name`, `booth_theme`, and `division_of_labor`.
2.  **Collect Activity Details**: Prompt the user to provide 3 to 5 specific actions performed during the event.
3.  **Collect Reflection Data**: Prompt the user to describe the `challenges` encountered and the corresponding `solutions` implemented.
4.  **Collect Competency Data**: Prompt the user to list the skills or abilities practiced (e.g., communication, teamwork, sustainability awareness).

### Phase 2: Image Integration
5.  **Map Images to Captions**:
    - Prompt the user for the local directory path containing the event photos.
    - Scan the directory and identify image files.
    - Sort the identified files numerically/alphabetically based on filenames.
    - For each identified file, prompt the user to provide a specific `caption`.

### Phase 3: Report Generation & Validation
6.  **Generate PDF Report**:
    - Synthesize all collected text and image-caption pairs into a structured PDF document.
    - Format the PDF with a clear hierarchy: Student Info $\rightarrow$ Activity Logs $\rightarrow$ Reflection $\rightarrow$ Competencies $\rightarrow$ Photo Gallery.
    - Save the file using the naming convention: `{name}_GreenMarket_Report.pdf`.
7.  **Validate File Size**:
    - Check the final PDF file size.
    - If the size is **less than 4MB**, confirm successful generation.
    - If the size is **4MB or greater**, notify the user of the failure and suggest optimization strategies (e.g., reducing image resolution or decreasing the number of images).

## Error Handling
- **Invalid Path**: If the provided image directory does not exist, prompt the user to re-enter a valid path.
- **Missing Data**: If mandatory fields (e.g., name, booth theme) are missing, re-prompt the user for the specific information.
- **Size Violation**: If the PDF exceeds 4MB, trigger the optimization advice workflow.
