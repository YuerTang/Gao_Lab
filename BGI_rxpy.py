import rx
from rx import operators as ops

goals = {'G1', 'G2', 'G3'}
InitialPriors = {'G1': 1/3, 'G2': 1/3, 'G3': 1/3}
likelihoods = {
    'G1': {'right': 0.95, 'down': 0.01, 'rightdown': 0.04},
    'G2': {'right': 0.05, 'down': 0.05, 'rightdown': 0.95},
    'G3': {'right': 0.01, 'down': 0.95, 'rightdown': 0.04}
}

def getPosterior(currentPriors, action, likelihoods):
    posterior = {goal: likelihoods[goal][action] * currentPriors[goal] for goal in currentPriors}
    total = sum(posterior.values())
    normalizedPosterior = {goal: posterior[goal] / total for goal in posterior}
    return normalizedPosterior

# convert the list of observed actions into an RxPy observable
observedActions = ['right', 'rightdown', 'down', 'down', 'right', 'rightdown']
observableActions = rx.from_(observedActions)
computePosteriorGivenAction= lambda currentPriors,action: getPosterior(currentPriors,action,likelihoods)
# create a data processing pipeline
updatedPriors = observableActions.pipe(
    ops.scan(lambda currentPriors, action: computePosteriorGivenAction(currentPriors,action), InitialPriors)
)

# Subscribe to the Observable to access and print the final updated probabilities
updatedPriors.subscribe(
    on_next=lambda x: print("Updated Priors:", x),

)
# Goal: instead of inputting the instructions of directions, actually combine keyboard compressing with rxpy so in the pipeline function first filter the strings, then get the directions, then use scan