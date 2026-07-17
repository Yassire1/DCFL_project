const pptxgen = require('pptxgenjs');
const html2pptx = require('./.opencode/skills/document-skills/pptx/scripts/html2pptx');
const fs = require('fs');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Yassire AMMOURI';
    pptx.title = 'Rapport d\'avancement de thèse';
    pptx.subject = 'Federated Time Series Foundation Models';

    const slidesDir = path.join(__dirname, 'phd_presentation', 'slides');
    const slideFiles = fs.readdirSync(slidesDir)
        .filter(f => f.endsWith('.html'))
        .sort((a, b) => {
            const numA = parseInt(a.replace('slide', '').replace('.html', ''));
            const numB = parseInt(b.replace('slide', '').replace('.html', ''));
            return numA - numB;
        });

    console.log(`Found ${slideFiles.length} HTML slides to convert`);

    for (const slideFile of slideFiles) {
        const slidePath = path.join(slidesDir, slideFile);
        console.log(`Converting ${slideFile}...`);
        
        try {
            await html2pptx(slidePath, pptx);
            console.log(`  ✓ ${slideFile}`);
        } catch (error) {
            console.error(`  ✗ ${slideFile}: ${error.message}`);
        }
    }

    const outputPath = path.join(__dirname, 'phd_presentation', 'PhD_Rapport_Avancement.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\n✅ Presentation saved to: ${outputPath}`);
}

createPresentation().catch(console.error);
