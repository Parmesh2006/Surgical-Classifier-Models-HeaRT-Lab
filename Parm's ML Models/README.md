<PHASE-ONE>
SELECT ONE INSTRUMENT:
    - SELECTION: _____________

Create a pipeline where it loads images, trains ResNet, gets good metrics, and AVOID OVERFITTING
    => ESSENTIALLY A BINARY CLASSIFIER (INSTRUMENT A vs NOT INSTRUMENT A)

Instrument A => 1
Not Instrument A => 0

Must accomplish:
    => Data loading works
    => ResNet training works
    => Validation metrics improve
    => Overfitting is controlled

Add these explicitly:
    => Train/val split (e.g., 80/20)
    => Data augmentation (VERY important)
    => Early stopping (prevent overfit)
</PHASE-ONE>

<PHASE-TWO>
REPEAT PHASE ONE FOR 2-3 INSTRUMENTS

GOAL: Check if the system works beyond one case
</PHASE-TWO>

<PHASE-THREE>
SWITCH TO MULTICLASS CLASSIFICATION EARLY [PRIORITIZE-THIS]

OR 

<WORST-CASE-SCENARIO>: Create 47 models (one for each of the 47 instruments, and combine them)
</PHASE-THREE>