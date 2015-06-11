#!/usr/bin/env python

# Built-in packages
import argparse
from argparse import RawDescriptionHelpFormatter
import logging

# Add-on packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# McLab packages
# import mclib


def getOptions():
    """ Function to pull in arguments """
    description = """ """
    parser = argparse.ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)

    group1 = parser.add_argument_group(description="Input Files")
    group1.add_argument("--input", dest="wide", action='store', required=True, help="Dataset in Wide format")

    group2 = parser.add_argument_group(description="Output Files")
    group2.add_argument("-o", dest="plot", action='store', required=True, help="Output of Mahalanobis distance plot")

    args = parser.parse_args()
    return(args)


def mahalnobisDistance(wide):
    """ Calculate the Mahalanobis distance and return an array of distances.

    Arguments:
        :type wide: pandas.DataFrame
        :param wide: A wide formatted data frame with samples as columns and compounds as rows.

    Returns:
        :return: Return a numpy array with MD values.
        :rtype: numpy.array
    """
    # Covariance matrix from the data
    covHat = wide.cov()

    # Inverse of the covariance matrix
    covHatInv = np.linalg.inv(covHat)

    # Column means
    colMean = wide.mean(axis=0)

    # Mean Center the data
    center = (wide - colMean).T

    # Calculate the mahalanobis distance sqrt{(Yi - Ybar)^T Sigma^-1 (Yi - Ybar)}
    MD = np.diag(np.sqrt(np.dot(np.dot(center.T, covHatInv), center)))

    # TODO: Maybe output the MD file in the future?
    return plotMahalanobis(MD)


def plotMahalanobis(MD):
    """ Plot the Mahalanobis distance plot.

    Arguments:
        :type MD: numpy.array
        :param MD: An array of distances.

    Returns:
        :return: Returns a figure object.
        :rtype: matplotlib.pyplot.Figure.figure

    """
    # Create figure object with a single axis
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    fig.suptitle('Mahalanobis Distance')

    # Plot MD as scatter plot
    ax.scatter(x=range(len(MD)), y=MD)
    ax.set_xlabel('Mean')
    ax.set_ylabel('Difference')

    # Add a horizontal line above 95% of the data
    ax.axhline(np.percentile(MD, 95), color='r', ls='--', lw=2)

    return fig


def main(args):
    """ Main Script """

    # TODO: May want to use the wideToDesign class. I know it seems like
    # overkill for this particular case, but I cannot guarantee that wide
    # datasets will never have additional columns (i.e., not just sampleIDs).
    # Perhaps we should talk with Morse and get her opinion.

    # Convert inputted wide file to dataframe
    df_wide = pd.DataFrame.from_csv(args.wide, sep='\t')
    figure = mahalnobisDistance(df_wide)

    figure.savefig(args.plot, bbox_inches='tight')

if __name__ == '__main__':
    # Turn on Logging if option -g was given
    args = getOptions()

    # Turn on logging
    logger = logging.getLogger()
    # if args.debug:
    #     mclib.logger.setLogger(logger, args.log, 'debug')
    # else:
    #     mclib.logger.setLogger(logger, args.log)

    # Output git commit version to log, if user has access
    # mclib.git.git_to_log(__file__)

    # Run Main part of the script
    main(args)
    logger.info("Script complete.")