"""
Report generation module for SmeHub API.
Contains the core logic for generating business reports.
"""

from pydantic import BaseModel
from datetime import datetime
import logging
import asyncio
from typing import List, Dict, Any
import json

# Import Claude and web search libraries
from anthropic import Anthropic
from tavily import TavilyClient

# Import configuration
from config import config

logger = logging.getLogger(__name__)

class BusinessInfo(BaseModel):
    businessName: str
    postalCode: str
    country: str
    industry: str

async def generate_business_report(business_info: BusinessInfo, prompt: str) -> str:
    """
    Generate a business report based on the provided business information and prompt.
    Uses Claude AI with web search for comprehensive analysis.
    
    Args:
        business_info: BusinessInfo object containing company details
        prompt: The user's specific request/prompt for the report
        
    Returns:
        str: The generated report content
    """
    logger.info(f"Generating AI-powered report for {business_info.businessName}")
    
    try:
        # Validate configuration
        config.validate_config()
        
        # Perform web search for market intelligence
        search_results = await _perform_web_search(business_info, prompt)
        
        # Generate report using Claude AI
        report_content = await _generate_claude_report(business_info, prompt, search_results)
        
        logger.info("AI report generation completed successfully")
        return report_content
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        # Fallback to basic report if AI fails
        logger.info("Falling back to basic report generation")
        return _create_fallback_report(business_info, prompt, str(e))

def generate_business_report_sync(business_info: BusinessInfo, prompt: str) -> str:
    """
    Synchronous wrapper for the async report generation function.
    """
    return asyncio.run(generate_business_report(business_info, prompt))

def _create_enhanced_report(business_info: BusinessInfo, prompt: str) -> str:
    """
    Private function to create the report content.
    This is where you'll add the actual AI integration.
    """
    
    # Enhanced dummy report with better structure
    # TODO: Replace with actual AI-generated content
    report = f"""
# Comprehensive Business Report for {business_info.businessName}

## Executive Summary
This report has been generated based on your specific requirements and business profile.

## Company Profile
- **Business Name**: {business_info.businessName}
- **Location**: {business_info.postalCode}, {business_info.country}
- **Industry Sector**: {business_info.industry}

## Request Analysis
**Your Request**: "{prompt}"

## Market Analysis
Based on your location in {business_info.country} and your operation in the {business_info.industry} sector, here are key insights:

### Industry Overview
- The {business_info.industry} sector shows various opportunities and challenges
- Location-specific factors in {business_info.country} may impact operations
- Market conditions should be monitored regularly

### Regional Considerations
- Operating in {business_info.postalCode} area
- Local market dynamics in {business_info.country}
- Regulatory environment considerations

## Strategic Recommendations

### Short-term Actions
1. Assess current market position in the {business_info.industry} sector
2. Evaluate local competition in {business_info.country}
3. Review operational efficiency measures

### Long-term Strategy
1. Consider expansion opportunities within {business_info.industry}
2. Develop market presence in {business_info.country}
3. Build sustainable competitive advantages

## Implementation Roadmap

### Phase 1: Assessment (Months 1-2)
- Market research and analysis
- Competitive landscape evaluation
- Internal capability assessment

### Phase 2: Strategy Development (Months 3-4)
- Strategic planning based on findings
- Resource allocation planning
- Risk assessment and mitigation

### Phase 3: Execution (Months 5-12)
- Implementation of strategic initiatives
- Performance monitoring and adjustment
- Continuous improvement processes

## Risk Assessment
- Industry-specific risks in {business_info.industry}
- Regional risks in {business_info.country}
- Operational risk factors

## Conclusion
This report provides a foundation for strategic decision-making for {business_info.businessName}. 
The analysis considers your specific industry context and geographical location to provide 
relevant insights and recommendations.

## Next Steps
1. Review recommendations with your team
2. Prioritize implementation actions
3. Establish monitoring and review processes

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*This is a template report. Replace with AI-generated content for production use.*
"""
    
    return report.strip()

async def _perform_web_search(business_info: BusinessInfo, prompt: str) -> List[Dict[str, Any]]:
    """
    Perform web search to gather market intelligence and current information.
    
    Args:
        business_info: Business information for context
        prompt: User's specific request
        
    Returns:
        List of search results with relevant market data
    """
    try:
        # Initialize Tavily client
        tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
        
        # Construct search queries based on business info and prompt
        search_queries = _build_search_queries(business_info, prompt)
        
        all_results = []
        
        for query in search_queries:
            logger.info(f"Searching for: {query}")
            
            # Perform search
            search_response = tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=config.MAX_SEARCH_RESULTS
            )
            
            # Extract useful information from search results
            if search_response and 'results' in search_response:
                for result in search_response['results']:
                    all_results.append({
                        'title': result.get('title', ''),
                        'content': result.get('content', ''),
                        'url': result.get('url', ''),
                        'score': result.get('score', 0),
                        'query': query
                    })
        
        logger.info(f"Found {len(all_results)} search results")
        return all_results
        
    except Exception as e:
        logger.error(f"Web search failed: {str(e)}")
        return []

def _build_search_queries(business_info: BusinessInfo, prompt: str) -> List[str]:
    """
    Build targeted search queries based on business information and user prompt.
    """
    queries = []
    
    # Industry-specific queries
    queries.append(f"{business_info.industry} industry trends 2024 {business_info.country}")
    queries.append(f"{business_info.industry} market analysis {business_info.country}")
    
    # Location-specific queries
    queries.append(f"business environment {business_info.country} {business_info.industry}")
    queries.append(f"regulations {business_info.industry} {business_info.country}")
    
    # Prompt-specific query
    if prompt:
        queries.append(f"{prompt} {business_info.industry} {business_info.country}")
    
    # Competitive landscape
    queries.append(f"competitors {business_info.industry} {business_info.country}")
    
    return queries

async def _generate_claude_report(business_info: BusinessInfo, prompt: str, search_results: List[Dict[str, Any]]) -> str:
    """
    Generate a comprehensive business report using Claude AI with search data.
    
    Args:
        business_info: Business information
        prompt: User's specific request
        search_results: Web search results for context
        
    Returns:
        AI-generated business report
    """
    try:
        # Initialize Claude client
        claude_client = Anthropic(api_key=config.CLAUDE_API_KEY)
        
        # Prepare context from search results
        search_context = _prepare_search_context(search_results)
        
        # Create comprehensive prompt for Claude
        claude_prompt = _build_claude_prompt(business_info, prompt, search_context)
        
        logger.info("Generating report with Claude AI")
        
        # Generate report using Claude
        response = claude_client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=config.CLAUDE_MAX_TOKENS,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": claude_prompt
                }
            ]
        )
        
        # Extract and return the generated report
        report_content = response.content[0].text
        
        logger.info("Claude AI report generation successful")
        return report_content
        
    except Exception as e:
        logger.error(f"Claude AI generation failed: {str(e)}")
        raise

def _prepare_search_context(search_results: List[Dict[str, Any]]) -> str:
    """
    Prepare search results as context for Claude AI.
    """
    if not search_results:
        return "No current market data available."
    
    context_parts = []
    
    # Group results by query for better organization
    query_groups = {}
    for result in search_results:
        query = result.get('query', 'general')
        if query not in query_groups:
            query_groups[query] = []
        query_groups[query].append(result)
    
    for query, results in query_groups.items():
        context_parts.append(f"\n=== Search Results for: {query} ===")
        
        for result in results[:3]:  # Limit to top 3 results per query
            if result.get('content'):
                context_parts.append(f"Title: {result.get('title', 'N/A')}")
                context_parts.append(f"Content: {result.get('content', '')[:500]}...")  # Limit content length
                context_parts.append(f"Source: {result.get('url', 'N/A')}")
                context_parts.append("---")
    
    return "\n".join(context_parts)

def _build_claude_prompt(business_info: BusinessInfo, user_prompt: str, search_context: str) -> str:
    """
    Build a comprehensive prompt for Claude AI.
    """
    return f"""
You are a senior business analyst tasked with creating a comprehensive business report. Use the provided information to generate a detailed, professional report.

BUSINESS INFORMATION:
- Company Name: {business_info.businessName}
- Location: {business_info.postalCode}, {business_info.country}
- Industry: {business_info.industry}

USER REQUEST:
{user_prompt}

CURRENT MARKET INTELLIGENCE:
{search_context}

INSTRUCTIONS:
1. Create a professional business report in markdown format
2. Use the current market intelligence to provide accurate, up-to-date insights
3. Include specific recommendations based on the company's industry and location
4. Structure the report with clear sections and actionable insights
5. Focus on practical, implementable strategies
6. Include risk assessments and market opportunities
7. Cite relevant information from the search results when appropriate
8. Make the report specific to the user's request while maintaining comprehensive coverage

REPORT STRUCTURE:
- Executive Summary
- Company Profile
- Market Analysis (use current data from search results)
- Industry Insights
- Competitive Landscape
- Strategic Recommendations
- Risk Assessment
- Implementation Roadmap
- Conclusion and Next Steps

Generate a detailed, professional report that provides real value to the business owner.
"""

def _create_fallback_report(business_info: BusinessInfo, prompt: str, error_message: str) -> str:
    """
    Create a fallback report when AI generation fails.
    """
    return f"""
# Business Report for {business_info.businessName}

## Notice
This report was generated using a fallback method due to a technical issue with the AI service.
Error: {error_message}

## Company Profile
- **Business Name**: {business_info.businessName}
- **Location**: {business_info.postalCode}, {business_info.country}
- **Industry**: {business_info.industry}

## User Request
{prompt}

## Basic Analysis
This is a basic report template. For a comprehensive AI-powered analysis with current market data, please ensure your API configuration is correct and try again.

### Industry Context
Your business operates in the {business_info.industry} sector in {business_info.country}. 

### Recommendations
1. Review your market position within the {business_info.industry} industry
2. Analyze local competition in {business_info.country}
3. Consider current market trends affecting your sector
4. Evaluate opportunities for growth and expansion

### Next Steps
1. Verify API configuration settings
2. Check internet connectivity for web search functionality
3. Retry report generation once technical issues are resolved

---
*Fallback report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*For full AI-powered analysis, please resolve the technical issue and regenerate the report.*
"""
