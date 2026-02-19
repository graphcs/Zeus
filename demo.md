Launch the UI                                                                                                                                                                  
                                                                                                                                                                                 
  uv run streamlit run ui.py                                                                                                                                                     
                                                                                                                                                                                 
  This opens in your browser (typically http://localhost:8501).                                                                                                                  
                                                                                                                                                                                 
  UI Layout                                                                                                                                                                      
                                                                                                                                                                                 
  The UI has 3 tabs:                                                                                                                                                             
  ┌─────────────────┬──────────────────────────────────────────────────┐                                                                                                         
  │       Tab       │                     Purpose                      │                                                                                                         
  ├─────────────────┼──────────────────────────────────────────────────┤                                                                                                         
  │ Design Brief    │ Generate a brief from an idea (Brief mode)       │                                                                                                         
  ├─────────────────┼──────────────────────────────────────────────────┤                                                                                                         
  │ Target Solution │ Generate a solution from a brief (Solution mode) │                                                                                                         
  ├─────────────────┼──────────────────────────────────────────────────┤                                                                                                         
  │ History         │ View past runs with full output                  │                                                                                                         
  └─────────────────┴──────────────────────────────────────────────────┘                                                                                                         
  There's also an "Advanced Budget Settings" toggle in the sidebar to control max LLM calls and timeout.                                                                         
                                                                                                                                                                                 
  Demo Walkthrough in the UI                                                                                                                                                     
                                                                                                                                                                                 
  1. V0 + V1 (automatic on every run)                                                                                                                                            
                                                                                                                                                                                 
  1. Go to the Design Brief tab                                                                                                                                                  
  2. Enter a prompt, e.g.: Design an AI-powered customer support platform                                                                                                        
  3. Add constraints (one per line):                                                                                                                                             
  Must handle 1M tickets/month                                                                                                                                                   
  Must comply with GDPR                                                                                                                                                          
  Must have 99.9% uptime SLA                                                                                                                                                     
  4. Optionally upload context files (.md, .txt, .pdf, .docx)                                                                                                                    
  5. Click "Generate Brief"                                                                                                                                                      
                                                                                                                                                                                 
  After it completes, the page will show:                                                                                                                                        
  - The main output (markdown rendered)                                                                                                                                          
  - V1 Evaluation section — confidence, coverage %, issue breakdown, covered/missing perspectives                                                                                
  - Design Tradeoffs section                                                                                                                                                     
  - Assumptions and Known Issues                                                                                                                                                 
  - Usage stats (LLM calls, tokens, cost)                                                                                                                                        
                                                                                                                                                                                 
  2. V3 — Constraint Verification + Structured Issues                                                                                                                            
                                                                                                                                                                                 
  This appears automatically because you added constraints. You'll see:                                                                                                          
  - "Constraints Verification (V3)" — with a coverage percentage and an expandable "Detailed Checks" section showing each constraint as PASS/FAIL/UNVERIFIED with evidence       
  - "Known Issues Registry (V3)" — expandable items each showing Impact, Mitigation, and Verification Step                                                                       
                                                                                                                                                                                 
  3. V2 — Regression Analysis                                                                                                                                                    
                                                                                                                                                                                 
  1. After the first run completes, click "Set as Baseline" (next to the Download button)                                                                                        
  2. Re-run the same prompt and constraints by clicking "Generate Brief" again                                                                                                   
  3. The second run will show a "V2 Regression Analysis" section at the top with:                                                                                                
    - Green success or red error banner                                                                                                                                          
    - Coverage delta, issues delta, constraints delta, blockers/majors as metrics                                                                                                
                                                                                                                                                                                 
  4. Solution Mode                                                                                                                                                               
                                                                                                                                                                                 
  1. Click "Download Brief" to save the brief as markdown                                                                                                                        
  2. Switch to the Target Solution tab                                                                                                                                           
  3. Upload the brief file (or paste it), add constraints                                                                                                                        
  4. Click "Generate Solution"                                                                                                                                                   
  5. Same V1/V2/V3 panels appear for the solution output                                                                                                                         
                                                                                                                                                                                 
  5. History Tab                                                                                                                                                                 
                                                                                                                                                                                 
  Click History → Refresh History to browse all past runs. Each run is expandable with a "View Output" button that renders the full response with all V1/V2/V3 panels.           
                                                                                                                                                                                 
  Demo Tips                                                                                                                                                                      
                                                                                                                                                                                 
  - The UI renders everything as formatted markdown with expandable sections — much more client-friendly than the CLI                                                            
  - The Download buttons export the full output + evaluation summary as a .md file the client can keep                                                                           
  - Use the sidebar budget controls if you want to show how the system operates under tighter constraints                                                                        
  - File upload supports .pdf and .docx in addition to text, which is useful for showing real-world input scenarios                                                              
                                                                                                                                                                                 
❯ what do I do for   3. Upload the brief file (or paste it), add constraints                                                                                                     
                        which constraints do I add                                                                                                                               
                                                                                                                                                                                 
⏺ Re-use the same constraints you used when generating the brief. The solution should be verified against the same requirements. So if your brief was:                           
                                                                                                                                                                                 
  Must handle 1M tickets/month                                                                                                                                                   
  Must comply with GDPR                                                                                                                                                          
  Must have 99.9% uptime SLA                                                                                                                                                     
                                                                                                                                                                                 
  Paste those same three lines into the constraints box on the Target Solution tab.                                                                                              
                                                                                                                                                                                 
  You can also add solution-specific constraints if you want to show the V3 verification getting more granular at the solution stage. For example:                               
                                                                                                                                                                                 
  Must handle 1M tickets/month                                                                                                                                                   
  Must comply with GDPR                                                                                                                                                          
  Must have 99.9% uptime SLA                                                                                                                                                     
  Must use containerized deployment                                                                                                                                              
  Must support horizontal scaling                                                                                                                                                
                                                                                                                                                                                 
  This is actually a good demo moment — you can point out to the client that the V3 Constraints Verification panel now covers more checks than the brief did, showing how        
  constraints can be progressively tightened as the design matures from brief to solution.                                                                                       
                                                                                               