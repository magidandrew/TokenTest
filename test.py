from Visualisation import revenue_cost_time, difficulty_time, alpha_revenue

'''revenue_cost_time(nb_simulations=17136, strat="ISM", revenue=[0, 3, 0, 4, 0, 5, 0, 10, 0], cost=[
                  1, 2, 1, 2, 1, 5, 1, 6, 1], alpha=0.4, gamma=0.3, window_size=2016)'''

'''difficulty_time(nb_simulations=21168, strat='Intermittent Selfish Mining', difficulty_list=[
                1, 0.9, 1.1, 0.7, 0.2, 0.9, 1.2, 0.6, 1.5, 0.8, 1.3], alpha=0.4, gamma=0.3, window_size=2016)
'''
alpha_revenue(strat='Intermittent Selfish Mining', revenue_mean_list=[0, 2016, 5034, 6910, 6920, 8033, 11249, 15904, 20102, 20160, 21942], cost_mean_list=[
              0, 1203, 3019, 4127, 4124, 5100, 5919, 6129, 8198, 11227, 12111], alpha_list=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], gamma=0.3)
