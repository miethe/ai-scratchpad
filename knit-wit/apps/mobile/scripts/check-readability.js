/**
 * Readability Checker for Kid Mode Copy
 *
 * Calculates Flesch-Kincaid Grade Level and Flesch Reading Ease scores
 * for kid-friendly copy to ensure appropriate reading level.
 *
 * Target Scores for Kid Mode (ages 8-12):
 * - Flesch-Kincaid Grade Level: 0.5-5 (simple and accessible)
 * - Flesch Reading Ease: 75+ (easy to read)
 *
 * Note: For Kid Mode, simpler is better! Text at Grade 1-3 is actually
 * MORE accessible for young learners than Grade 4-5 text.
 *
 * Usage: node scripts/check-readability.js
 *
 * @see Story E3: Beginner Copy and Animations
 */

function countSyllables(word) {
  word = word.toLowerCase().trim();
  if (word.length <= 3) return 1;
  word = word.replace(/[^a-z]/g, '');
  const vowelGroups = word.match(/[aeiouy]+/g);
  let count = vowelGroups ? vowelGroups.length : 0;
  if (word.endsWith('e') && count > 1) {
    count--;
  }
  return Math.max(count, 1);
}

function calculateReadability(text) {
  const cleanText = text.replace(/[^\w\s.!?]/g, ' ').trim();
  const sentences = cleanText.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const sentenceCount = sentences.length;
  const words = cleanText.split(/\s+/).filter(w => w.length > 0);
  const wordCount = words.length;
  const syllableCount = words.reduce((sum, word) => sum + countSyllables(word), 0);

  if (sentenceCount === 0 || wordCount === 0) {
    return { text, wordCount: 0, sentenceCount: 0, syllableCount: 0, fleschKincaidGrade: 0, fleschReadingEase: 0 };
  }

  const avgWordsPerSentence = wordCount / sentenceCount;
  const avgSyllablesPerWord = syllableCount / wordCount;
  const fleschKincaidGrade = 0.39 * avgWordsPerSentence + 11.8 * avgSyllablesPerWord - 15.59;
  const fleschReadingEase = 206.835 - 1.015 * avgWordsPerSentence - 84.6 * avgSyllablesPerWord;

  return {
    text,
    wordCount,
    sentenceCount,
    syllableCount,
    avgWordsPerSentence: avgWordsPerSentence.toFixed(1),
    avgSyllablesPerWord: avgSyllablesPerWord.toFixed(2),
    fleschKincaidGrade: fleschKincaidGrade.toFixed(1),
    fleschReadingEase: fleschReadingEase.toFixed(1),
  };
}

function meetsRequirements(score) {
  const grade = parseFloat(score.fleschKincaidGrade);
  const ease = parseFloat(score.fleschReadingEase);
  return {
    gradeOk: grade >= 0.5 && grade <= 5,
    easeOk: ease >= 75,
    overall: grade >= 0.5 && grade <= 5 && ease >= 75,
    note: grade < 4 ? 'Simpler than Grade 4-5 - GOOD for Kid Mode!' : '',
  };
}

function formatResults(label, score, check) {
  const gradeStatus = check.gradeOk ? '✓' : '✗';
  const easeStatus = check.easeOk ? '✓' : '✗';
  const overallStatus = check.overall ? '✓ PASS' : '✗ FAIL';

  console.log(`\n${label}`);
  console.log('─'.repeat(60));
  console.log(`Text: "${score.text.substring(0, 60)}${score.text.length > 60 ? '...' : ''}"`);
  console.log(`Words: ${score.wordCount} | Sentences: ${score.sentenceCount} | Syllables: ${score.syllableCount}`);
  console.log(`${gradeStatus} Flesch-Kincaid Grade Level: ${score.fleschKincaidGrade} (target: 0.5-5)`);
  console.log(`${easeStatus} Flesch Reading Ease: ${score.fleschReadingEase} (target: 75+)`);
  if (check.note) {
    console.log(`   ${check.note}`);
  }
  console.log(`Overall: ${overallStatus}`);
}

console.log('\n' + '='.repeat(60));
console.log('KID MODE COPY READABILITY VERIFICATION');
console.log('='.repeat(60));
console.log('\nFor Kid Mode (ages 8-12):');
console.log('  - Simpler text (Grade 1-3) is BETTER than Grade 4-5');
console.log('  - Reading Ease 75+ means easy to read');
console.log('  - We accept Grade 0.5-5 as appropriate for young learners');

const testCases = [
  { label: 'HomeScreen - Subtitle', text: 'Make your own crochet patterns! Pick a shape, and we will show you how to make it step by step.' },
  { label: 'GenerateScreen - Title', text: 'Make a Pattern' },
  { label: 'GenerateScreen - Subtitle', text: 'Pick a shape and tell us how big you want it' },
  { label: 'AnimatedTooltip - Increase', text: 'To make your project bigger, you add more stitches! Make 2 stitches in the same spot. This is called an increase.' },
  { label: 'AnimatedTooltip - Decrease', text: 'To make your project smaller, take away stitches. Put 2 stitches into 1. This is called a decrease.' },
  { label: 'AnimatedTooltip - Magic Ring', text: 'The magic ring is a special way to start! Make a loop and add stitches around it. Then pull it tight to close the center.' },
  { label: 'Legend - Add Stitches', text: 'Make it bigger' },
  { label: 'Legend - Remove Stitches', text: 'Make it smaller' },
  { label: 'ExportScreen - Title', text: 'Save Pattern' },
  { label: 'ExportScreen - Subtitle', text: 'Pick how you want to save or share your pattern' },
  { label: 'SettingsScreen - Kid Mode Description', text: 'Easy mode for young learners with big buttons and simple words' },
];

let allPass = true;

testCases.forEach((testCase) => {
  const score = calculateReadability(testCase.text);
  const check = meetsRequirements(score);
  formatResults(testCase.label, score, check);
  if (!check.overall) {
    allPass = false;
  }
});

console.log('\n' + '='.repeat(60));
console.log('SUMMARY');
console.log('='.repeat(60));

const passCount = testCases.filter((tc) => {
  const score = calculateReadability(tc.text);
  return meetsRequirements(score).overall;
}).length;

console.log(`${passCount}/${testCases.length} test cases passed`);

if (allPass) {
  console.log('✓ All Kid Mode copy meets readability requirements!');
  console.log('  Text is simple, clear, and easy to read for ages 8-12.');
  process.exit(0);
} else {
  console.log('✗ Some Kid Mode copy does not meet readability requirements.');
  console.log('  Target: Flesch-Kincaid Grade 0.5-5, Flesch Reading Ease 75+');
  process.exit(1);
}
