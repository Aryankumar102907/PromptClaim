import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message, sessionId } = await request.json();

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    // Mock AI response based on legal keywords
    let response = '';
    
    const legalKeywords = {
      contract: "Regarding contract law, it's important to understand the key elements: offer, acceptance, consideration, and mutual assent. I recommend reviewing all terms carefully and ensuring both parties understand their obligations.",
      
      employment: "Employment law covers various aspects including wrongful termination, discrimination, wage and hour disputes, and workplace safety. Each case depends on specific circumstances and applicable state/federal laws.",
      
      intellectual: "Intellectual property protection includes patents, trademarks, copyrights, and trade secrets. The type of protection needed depends on your specific intellectual property and business goals.",
      
      real: "Real estate transactions involve multiple legal considerations including title searches, property disclosures, financing terms, and closing procedures. It's crucial to review all documentation thoroughly.",
      
      corporate: "Corporate compliance requires adherence to various regulations depending on your business structure, industry, and jurisdiction. Regular legal audits can help ensure ongoing compliance.",
      
      litigation: "Litigation involves complex procedures and strict deadlines. Early case assessment and strategic planning are crucial for successful outcomes.",
      
      default: "Thank you for your legal inquiry. Based on your question, I recommend consulting with a qualified attorney who specializes in the relevant area of law. I can help you understand general legal concepts and prepare questions for your consultation."
    };

    // Simple keyword matching for demo purposes
    const messageLower = message.toLowerCase();
    
    if (messageLower.includes('contract')) {
      response = legalKeywords.contract;
    } else if (messageLower.includes('employment') || messageLower.includes('job') || messageLower.includes('termination')) {
      response = legalKeywords.employment;
    } else if (messageLower.includes('intellectual') || messageLower.includes('patent') || messageLower.includes('trademark')) {
      response = legalKeywords.intellectual;
    } else if (messageLower.includes('real estate') || messageLower.includes('property') || messageLower.includes('purchase')) {
      response = legalKeywords.real;
    } else if (messageLower.includes('corporate') || messageLower.includes('compliance') || messageLower.includes('sec')) {
      response = legalKeywords.corporate;
    } else if (messageLower.includes('litigation') || messageLower.includes('lawsuit') || messageLower.includes('court')) {
      response = legalKeywords.litigation;
    } else {
      response = legalKeywords.default;
    }

    // Add a personalized touch
    response += `\n\nIf you have specific details about your situation, please feel free to share them, and I can provide more targeted guidance. Remember, this is general information and not a substitute for professional legal advice.`;

    return NextResponse.json({ 
      response,
      sessionId,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Failed to process your request. Please try again.' },
      { status: 500 }
    );
  }
}