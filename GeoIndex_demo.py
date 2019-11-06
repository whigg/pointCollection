{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 236,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The autoreload extension is already loaded. To reload it, use:\n",
      "  %reload_ext autoreload\n"
     ]
    }
   ],
   "source": [
    "%load_ext autoreload\n",
    "%autoreload 2;"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 252,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pointCollection as pc\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import os\n",
    "import glob"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# The geoIndex class\n",
    "The GeoIndex class is designed to allow us to find data for a specific area from a file or a collection of files.  It works by subdividing the data into bins, and keeping track of where in a file each particular bin is found.  To illustrate how it works, we will make a simple data set, and generate an index for it."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First, we'll generate a set of data:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 253,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(-54.95, 53.95, -10.99, 10.790000000000001)"
      ]
     },
     "execution_count": 253,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXkAAAD4CAYAAAAJmJb0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAQyUlEQVR4nO3df6zddX3H8eeL4sVlZkGhaO2PlWTdAopTc8No/IdZnOgMdUMStsU2StKYYCaJywBJ5pZJgjFR5vyRNWqGCQ6JyGgUo9DRzCX8sCiigEqnUSoMqvPXQsJNy3t/nG/LaTnt7b3nnHt6Pvf5SG56vp/v93w/n0+avu6nn+/73JuqQpLUppMmPQBJ0vgY8pLUMENekhpmyEtSwwx5SWrYyZMeQL/TTz+91q9fP+lhSNJUuf/++39WVSsHnTuhQn79+vXs3r170sOQpKmS5MdHO+d2jSQ1zJCXpIYZ8pLUMENekhpmyEtSwwx5SWqYIS9JDTPkJalhhrwkNcyQl6SGGfKS1LChQz7JC5Pcl+TbSR5K8g9d+5lJ7k3yaJLPJ5kZfriSpIUYxUr+GeD1VfWHwKuBC5OcB3wQ+EhVbQB+AVw2gr4kSQswdMhXz/91hy/ovgp4PfCFrv0G4K3D9iVJWpiR7MknWZHkAeAp4A7gv4FfVtX+7pK9wOpR9CVJOn4jCfmqOlBVrwbWAOcCZw26bNB7k2xLsjvJ7n379o1iOJKkzkira6rql8Au4Dzg1CQHfynJGuDxo7xne1XNVtXsypUDf7GJJGmRRlFdszLJqd3r3wIuAB4B7gLe1l22Fbht2L4kSQszil//twq4IckKet80bq6qLyV5GLgpyQeAbwGfHkFfkqQFGDrkq+pB4DUD2n9Ib39ekjQhfuJVkhpmyEtSwwx5SWqYIS9JDTPkJalhhrwkNcyQl6SGGfKS1DBDXpIaZshLUsMMeUlqmCEvSQ0z5CWpYYa8JDXMkJekhhnyktQwQ16SGmbIS1LDDHlJapghL0kNM+QlqWGGvCQ1bOiQT7I2yV1JHknyUJL3dO0vSXJHkke7P188/HAlSQsxipX8fuC9VXUWcB5weZKzgauAnVW1AdjZHUuSltDQIV9VT1TVN7vXvwEeAVYDm4EbustuAN46bF+SpIUZ6Z58kvXAa4B7gZdW1RPQ+0YAnHGU92xLsjvJ7n379o1yOJK07I0s5JO8CLgFuKKqfn2876uq7VU1W1WzK1euHNVwJEmMKOSTvIBewN9YVV/smp9Msqo7vwp4ahR9SZKO3yiqawJ8Gnikqj7cd2oHsLV7vRW4bdi+JEkLc/II7vE64O3Ad5I80LW9D7gOuDnJZcBPgEtG0JckaQGGDvmq+i8gRzm9adj7S5IWz0+8SlLDDHlJapghL0kNM+QlqWGGvCQ1zJCXpIYZ8pLUMENekhpmyEtSwwx5SWqYIS9JDTPkJalhhrwkNcyQl6SGGfKS1DBDXpIaZshLUsMMeUlqmCEvSQ0z5CWpYYa8JDXMkJekho0k5JN8JslTSb7b1/aSJHckebT788Wj6EuSdPxGtZL/V+DCI9quAnZW1QZgZ3csSVpCJ4/iJlX1n0nWH9G8GTi/e30DsAu4chT9SdK0u/vuu9m1axfnn38+wKHXGzduHGk/Iwn5o3hpVT0BUFVPJDlj0EVJtgHbANatWzfG4UjS0hsU5qeddhpXXHEFc3NzrFixgiTs37+fmZkZdu7cOdKgH2fIH5eq2g5sB5idna0JD0eShnJkqG/atOl5YZ6EZ5999tAXQFUxNzfHrl27pibkn0yyqlvFrwKeGmNfkrSk5luhz8zMsHXrVubm5jhw4MBhYX7SSScdCv0jV/IH7zcq4wz5HcBW4Lruz9vG2Jckjd3BYD/adkv/Cn1ubg6AmZmZgdsy119/PT//+c/HviefquF3SJL8G72HrKcDTwLvB/4duBlYB/wEuKSq/vdY95mdna3du3cPPR5JGsZ8q/T+ME8CHL5Cf/bZZw/trx98/zjDPMn9VTU78NwoQn5UDHlJS2khD0X7g70/zI+1Qh/1qvxojhXyE3/wKklLaSFbLkfbR1/K7ZZhGfKSmrSQLZfjfSh6rFX6iRbuBxnykqbasFsu84X5wXueiKv042HIS5o6S73lMo3hfpAhL+mEdLSP/cNzHzBaLlsuwzDkJZ0w5luhH/kBo+Wy5TIMQ17SklvsQ9EjP2C0XLZchmGdvKSxGUcd+pEfMFqu4d3POnlJS2apHooa7sfHkJe0KNahTwdDXtIxWYc+3Qx5Sc9jHXo7DHlpmbIOfXkw5KVlxDr05ceQlxpkHboOsk5emmLWoQusk5eaYh26FsKQl05Q1qFrFAx5acKsQ9c4GfLSBFiHrqViyEtj0r9C37hx48Bgd8tF42bISyM0KMgPBvOgYHfLReM29pBPciHwT8AK4FNVdd24+5TGbSEPRefm5rjlllsGfsDILReN21hDPskK4OPAG4C9wDeS7Kiqh8fZrzQqo3goOjMzw8UXX8zXv/71gR8wMsw1TuNeyZ8L7KmqHwIkuQnYDBjyOmGN46Hoxo0bOeecc9xy0ZIbd8ivBh7rO94L/FH/BUm2AdsA1q1bN+bhSM+ZRB264a6lNu6Qz4C2w36OQlVtB7ZD78cajHk8WoasQ9dyNu6Q3wus7TteAzw+5j4l69ClzrhD/hvAhiRnAj8FLgX+csx9apmwDl2a31hDvqr2J3k38FV6JZSfqaqHxtmn2mYdurQwY6+Tr6rbgdvH3Y/aYh26NBp+4lUTZR26NF6GvJacdejS0jHkNTbWoUuTZ8hraNahSycuQ16LYh26NB0MeR2Tv4JOmm6GvA5zZKhv2rTJLRdpihnyy9R8K/SZmRm2bt16qPbcLRdpOhnyjVvsQ9G5uTkAZmZmnnedWy7S9DDkGzSqh6Jbtmxhy5Ytz/sm4ZaLND0M+Sm2VA9F+wPdcJemiyE/BaxDl7RYhvwJyjp0SaNgyE+YdeiSxsmQX2LWoUtaSob8mFiHLulEYMgPyTp0SScyQ34RrEOXNC0M+WOwDl3StDPksQ5dUruWbchbhy5pORgq5JNcAvw9cBZwblXt7jt3NXAZcAD466r66jB9LZZ16JKWs2FX8t8F/hz4l/7GJGcDlwKvAF4O3Jnk96vqwJD9zcs6dEl6zlAhX1WPACQ58tRm4Kaqegb4UZI9wLnA3cP0dzSDtl6sQ5ek8e3Jrwbu6Tve27WN3N13331otW4duiQdbt6QT3In8LIBp66pqtuO9rYBbXWU+28DtgGsW7duvuE8z65duw6t1q1Dl6TDzRvyVXXBIu67F1jbd7wGePwo998ObAeYnZ0d+I3gWM4///xDq3Xr0CXpcOPartkBfC7Jh+k9eN0A3DeOjjZu3MjOnTtdoUvSAMOWUP4Z8M/ASuDLSR6oqjdW1UNJbgYeBvYDl4+zsmbjxo2GuyQNMGx1za3ArUc5dy1w7TD3lyQN56RJD0CSND6GvCQ1zJCXpIYZ8pLUMENekhpmyEtSwwx5SWqYIS9JDTPkJalhhrwkNcyQl6SGGfKS1DBDXpIaZshLUsMMeUlqmCEvSQ0z5CWpYYa8JDXMkJekhhnyktQwQ16SGmbIS1LDhgr5JB9K8r0kDya5NcmpfeeuTrInyfeTvHH4oUqSFmrYlfwdwCur6lXAD4CrAZKcDVwKvAK4EPhEkhVD9iVJWqChQr6qvlZV+7vDe4A13evNwE1V9UxV/QjYA5w7TF+SpIUb5Z78O4GvdK9XA4/1ndvbtT1Pkm1JdifZvW/fvhEOR5J08nwXJLkTeNmAU9dU1W3dNdcA+4EbD75twPU16P5VtR3YDjA7OzvwGknS4swb8lV1wbHOJ9kKvAXYVFUHQ3ovsLbvsjXA44sdpCRpcYatrrkQuBK4qKqe7ju1A7g0ySlJzgQ2APcN05ckaeHmXcnP42PAKcAdSQDuqap3VdVDSW4GHqa3jXN5VR0Ysi9J0gINFfJV9XvHOHctcO0w95ckDcdPvEpSwwx5SWqYIS9JDTPkJalhhrwkNcyQl6SGGfKS1DBDXpIaZshLUsMMeUlqmCEvSQ0z5CWpYYa8JDXMkJekhhnyktQwQ16SGmbIS1LDDHlJapghL0kNM+QlqWGGvCQ1zJCXpIYNFfJJ/jHJg0keSPK1JC/v2pPko0n2dOdfO5rhSpIWYtiV/Ieq6lVV9WrgS8Dfde1vAjZ0X9uATw7ZjyRpEYYK+ar6dd/hbwPVvd4MfLZ67gFOTbJqmL4kSQt38rA3SHItsAX4FfDHXfNq4LG+y/Z2bU8MeP82eqt91q1bN+xwJEl95l3JJ7kzyXcHfG0GqKprqmotcCPw7oNvG3CrGtBGVW2vqtmqml25cuVi5yFJGmDelXxVXXCc9/oc8GXg/fRW7mv7zq0BHl/w6CRJQxm2umZD3+FFwPe61zuALV2VzXnAr6rqeVs1kqTxGnZP/rokfwA8C/wYeFfXfjvwZmAP8DTwjiH7kSQtwlAhX1UXH6W9gMuHubckaXh+4lWSGmbIS1LDDHlJapghL0kNM+QlqWGGvCQ1zJCXpIYZ8pLUMENekhpmyEtSwwx5SWpYej9m5sSQZB+9H3Q2bU4HfjbpQUzAcpz3cpwzLM95T9Ocf7eqBv5CjhMq5KdVkt1VNTvpcSy15Tjv5ThnWJ7zbmXObtdIUsMMeUlqmCE/GtsnPYAJWY7zXo5zhuU57ybm7J68JDXMlbwkNcyQl6SGGfIjkORvklSS07vjJPlokj1JHkzy2kmPcVSSfCjJ97p53Zrk1L5zV3dz/n6SN05ynOOQ5MJubnuSXDXp8YxDkrVJ7krySJKHkryna39JkjuSPNr9+eJJj3XUkqxI8q0kX+qOz0xybzfnzyeZmfQYF8OQH1KStcAbgJ/0Nb8J2NB9bQM+OYGhjcsdwCur6lXAD4CrAZKcDVwKvAK4EPhEkhUTG+WIdXP5OL2/27OBv+jm3Jr9wHur6izgPODybp5XATuragOwsztuzXuAR/qOPwh8pJvzL4DLJjKqIRnyw/sI8LdA/xPszcBnq+ce4NQkqyYyuhGrqq9V1f7u8B5gTfd6M3BTVT1TVT8C9gDnTmKMY3IusKeqflhVc8BN9ObclKp6oqq+2b3+Db3QW01vrjd0l90AvHUyIxyPJGuAPwU+1R0HeD3whe6SqZ2zIT+EJBcBP62qbx9xajXwWN/x3q6tNe8EvtK9bn3Orc/veZKsB14D3Au8tKqegN43AuCMyY1sLK6nt1h7tjs+Dfhl34Jmav++T570AE50Se4EXjbg1DXA+4A/GfS2AW1TU6t6rDlX1W3dNdfQ+6/9jQffNuD6qZnzcWh9fodJ8iLgFuCKqvp1b2HbpiRvAZ6qqvuTnH+wecClU/n3bcjPo6ouGNSe5BzgTODb3T+ANcA3k5xL77v+2r7L1wCPj3moI3O0OR+UZCvwFmBTPfdBi6me83FofX6HJHkBvYC/saq+2DU/mWRVVT3RbT0+NbkRjtzrgIuSvBl4IfA79Fb2pyY5uVvNT+3ft9s1i1RV36mqM6pqfVWtpxcCr62q/wF2AFu6KpvzgF8d/K/utEtyIXAlcFFVPd13agdwaZJTkpxJ76HzfZMY45h8A9jQVVzM0HvIvGPCYxq5bi/608AjVfXhvlM7gK3d663AbUs9tnGpqqurak337/hS4D+q6q+Au4C3dZdN7ZxdyY/H7cCb6T18fBp4x2SHM1IfA04B7uj+B3NPVb2rqh5KcjPwML1tnMur6sAExzlSVbU/ybuBrwIrgM9U1UMTHtY4vA54O/CdJA90be8DrgNuTnIZvUqySyY0vqV0JXBTkg8A36L3zW/q+GMNJKlhbtdIUsMMeUlqmCEvSQ0z5CWpYYa8JDXMkJekhhnyktSw/wfRw+E9hzptigAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# define a set of data points:\n",
    "x=np.arange(-50, 50, dtype=np.float64)\n",
    "y=0.2*x\n",
    "t=np.ones_like(x)\n",
    "plt.figure(1); plt.clf()\n",
    "plt.plot(x, y,'k.')\n",
    "plt.axis('equal')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we'll generate a geoIndex for the points, with 10-unit bins. We'll use the geoIndex.from_xy() method, which makes a geoIndex for based on the data locations."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 254,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pointCollection.geoIndex.geoIndex'> with 11 bins, referencing 1 files\n"
     ]
    }
   ],
   "source": [
    "gi=pc.geoIndex(delta=[10, 10]).from_xy([x, y])\n",
    "print(gi)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A geoIndex is just a subclass of a dict, so it has a keys() method.  Each key is the x and y coordinates of the bin, separated by an underscore.  "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 237,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "dict_keys(['0_0', '-10_0', '10_0', '-20_0', '20_0', '-30_-10', '30_10', '-40_-10', '40_10', '-50_-10', '50_10'])"
      ]
     },
     "execution_count": 237,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "gi.keys()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, let's plot the bin locations. The geoIndex.bins_as_array() method, which returns the locations of the bins in the geoIndex as a list of two arrays:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 238,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# plot the data and the bins\n",
    "plt.figure(1); plt.clf()\n",
    "plt.plot(x, y,'k.')\n",
    "xyb=gi.bins_as_array()\n",
    "plt.plot(xyb[0], xyb[1],'r*')\n",
    "plt.axis('equal');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can then query the geoIndex for the data associated with a particular bin. To get the data associated with the bin at (10, 0), we just index it with that bin's keys:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 216,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'file_num': array([0]), 'offset_start': array([56]), 'offset_end': array([64])}\n"
     ]
    }
   ],
   "source": [
    "Q=gi['10_0']\n",
    "print(Q)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This tells us that the data for the bin at (10,0) has indices between 56 and 64."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 217,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXkAAAD4CAYAAAAJmJb0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAASdElEQVR4nO3df4xdZZ3H8feXtsOPdaFSitS2Q0m2bkBx1Uy6TPynS1HRFaqLJOwaW5VklghZm2gEbLK6WRsxGmVdXOJEjZjURSIiVTFaKs26SQGLIliK0MUAlS5UUHRTYGj73T/umfa2vdP5ce6d2/vM+5VM5pznnHue5+mkn/vMc557JjITSVKZjut2AyRJnWPIS1LBDHlJKpghL0kFM+QlqWCzu92AZqeddlouWbKk282QpJ5y3333/S4z57c6dkyF/JIlS9i6dWu3myFJPSUiHh/rmNM1klQwQ16SCmbIS1LBDHlJKpghL0kFM+QlqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwWqHfEScEBH3RsQvI2JbRPxLVX5WRNwTEY9GxLcioq9+cyVJk9GOkfxLwPmZ+VfAG4ALI+I84DPAFzJzKfB74PI21CVJmoTaIZ8N/1ftzqm+Ejgf+HZVfhPwrrp1SZImpy1z8hExKyLuB54BNgL/A/whM/dWp+wEFrajLknSxLUl5DNzX2a+AVgELAPObnVaq9dGxFBEbI2Irbt3725HcyRJlbaursnMPwCbgfOAuREx+kdJFgFPjfGa4cwcyMyB+fNb/mETSdIUtWN1zfyImFttnwhcAGwH7gLeU522Gri9bl2SpMlpx5//WwDcFBGzaLxp3JKZ34+Ih4CbI+JTwC+Ar7ahLknSJNQO+cx8AHhji/LHaMzPS5K6xE+8SlLBDHlJKpghL0kFM+QlqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwQx5SSqYIS9JBTPkJalghrwkFcyQl6SCGfKSVDBDXpIKZshLUsEMeUkqmCEvSQUz5CWpYIa8JBXMkJekgtUO+YhYHBF3RcT2iNgWER+uyk+NiI0R8Wj1/ZX1mytJmox2jOT3Ah/JzLOB84ArI+Ic4BpgU2YuBTZV+5KkaVQ75DNzV2b+vNr+E7AdWAisBG6qTrsJeFfduiRJk9PWOfmIWAK8EbgHeFVm7oLGGwFw+hivGYqIrRGxdffu3e1sjiTNeG0L+Yh4BXArsCYz/zjR12XmcGYOZObA/Pnz29UcSRJtCvmImEMj4Ndn5neq4qcjYkF1fAHwTDvqkiRNXDtW1wTwVWB7Zn6+6dAGYHW1vRq4vW5dkqTJmd2Ga7wZeB/wYETcX5V9HLgOuCUiLgeeAC5tQ12SpEmoHfKZ+d9AjHF4Rd3rS5Kmzk+8SlLBDHlJKpghL0kFM+QlqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwQx5SSqYIS9JBTPkJalghrwkFcyQl6SCGfKSVDBDXpIKZshLUsEMeUkqmCEvSQUz5CWpYIa8JBXMkJekgrUl5CPiaxHxTET8qqns1IjYGBGPVt9f2Y66JEkT166R/NeBCw8ruwbYlJlLgU3VviRpGs1ux0Uy878iYslhxSuB5dX2TcBm4Op21CdJvW7Lli1s3ryZ5cuXAxzYHhwcbGs9bQn5MbwqM3cBZOauiDi91UkRMQQMAfT393ewOZI0/VqF+bx581izZg0jIyPMmjWLiGDv3r309fWxadOmtgZ9J0N+QjJzGBgGGBgYyC43R5JqOTzUV6xYcUSYRwT79+8/8AWQmYyMjLB58+aeCfmnI2JBNYpfADzTwbokaVqNN0Lv6+tj9erVjIyMsG/fvkPC/LjjjjsQ+oeP5Eev1y6dDPkNwGrguur77R2sS5I6bjTYx5puaR6hj4yMANDX19dyWub666/n2Wef7ficfGTWnyGJiP+kcZP1NOBp4BPAd4FbgH7gCeDSzHzuaNcZGBjIrVu31m6PJNUx3ii9OcwjAjh0hL5///4D8+ujr+9kmEfEfZk50PJYO0K+XQx5SdNpMjdFm4O9OcyPNkJv96h8LEcL+a7feJWk6TSZKZex5tGnc7qlLkNeUpEmM+Uy0ZuiRxulH2vhPsqQl9TT6k65jBfmo9c8FkfpE2HIS+o50z3l0ovhPsqQl3RMGutj/3DwA0YzZcqlDkNe0jFjvBH64R8wmilTLnUY8pKm3VRvih7+AaOZMuVSh+vkJXVMJ9ahH/4Bo5ka3s1cJy9p2kzXTVHDfWIMeUlT4jr03mDISzoq16H3NkNe0hFch14OQ16aoVyHPjMY8tIM4jr0mceQl3rU+gfXs3bTWp54/glOPfFUAJ574Tn6T+nn/Yvfz/GPHO86dLlOXuolo8H++POPEwTJGP9/X4b4XjDn4TmuQ58BXCcv9ZhWo/RnX3j2kGAfM+AB5kCen7z84MuNc12HPmMZ8lIXTSTMn33h2QPnHzXYD3cKzJkzx5uiM5whL02zsaZcphzmY5gbc7lj8x2AUy8zmSEvTaP1D65n6HtD7Hl5D9CeMG/lpDknccNFNzB4rlMvM91x3W6AVKotW7bw6U9/mi1bthzYv+o7Vx0I+HYIAoB5J85j3onzCIIzTzmT4YuGee+5721bPepdjuSlNmq1Dn10LnzNmjW88LEXqHJ5ykaneM485UzWrVhnmOuoOh7yEXEh8G/ALOArmXldp+uUOm0yD+caGRnh1ltvbaxBfx6YO7E6RsN83onzYP9+nnvx9/T/+SLWvfU6g10T1tGQj4hZwJeAtwA7gZ9FxIbMfKiT9Urt0o6Hc/X19XHJJZfw05/+lBd/8iJ5UcKcg3UcEuYc/EDTIaP0D30Ivvxl+MeLwIDXJHR6JL8M2JGZjwFExM3ASsCQ1zGrEw/nGhwc5Nxzz2Xz5s289JqX+PqTX+eJ5584MswPd+KJ8OKLB/dvvLHxdcIJ8MIL0/CvoV7X6ZBfCDzZtL8T+OvmEyJiCBgC6O/v73BzpIO68Tz00bJP8smJNfKxx+CjH4Xvfhf27IGTToJ3vxs+97l2/TOocJ0O+Va3mA5ZM5aZw8AwNB5r0OH2aAbq6eehL1gAJ5/cGM2fcELj+8knwxlntLceFavTIb8TWNy0vwh4qsN1SmU9D/3pp+GKK2BoCIaHYdeuztWl4nT0AWURMRt4BFgB/Bb4GfAPmbmt1fk+oEyT0TxCHxwcbBnszWEe0fjFsjnMWz2g62hTLtKxqGsPKMvMvRFxFfAjGksovzZWwEsTMd469MOD/ZiYcpG6qOPr5DPzDuCOTtejskx1Hfrhf+jimJlykbrET7yqq9q9Dr3VH7owzDWTGfKadp1eh+6Ui3SQIa+O6eY6dEkNhrxq6+l16FLhDHlNSVHr0KWCGfI6qm5MuUhqH0Nehzg81FesWOGUi9TDDPkZarwRel9fH6tXrz6w9twpF6k3GfKFm+pN0ZGREQD6+vqOOM8pF6l3GPIFatdN0VWrVrFq1aoj3iSccpF6hyHfw6brpmhzoBvuUm8x5HuA69AlTZUhf4xyHbqkdjDku8x16JI6yZCfZq5DlzSdDPkOcR26pGOBIV+T69AlHcsM+SlwHbqkXmHIH4Xr0CX1OkMe16FLKteMDXnXoUuaCWqFfERcCnwSOBtYlplbm45dC1wO7AP+KTN/VKeuqXIduqSZrO5I/lfA3wFfbi6MiHOAy4DXAq8G7oyI12Tmvpr1jct16JJ0UK2Qz8ztABFx+KGVwM2Z+RLwm4jYASwDttSpbyytpl5chy5JnZuTXwjc3bS/sypruy1bthwYrbsOXZIONW7IR8SdwBktDq3NzNvHelmLshzj+kPAEEB/f/94zTnC5s2bD4zWXYcuSYcaN+Qz84IpXHcnsLhpfxHw1BjXHwaGAQYGBlq+ERzN8uXLD4zWXYcuSYfq1HTNBuCbEfF5GjdelwL3dqKiwcFBNm3a5Ahdklqou4Ty3cC/A/OBH0TE/Zn5tszcFhG3AA8Be4ErO7myZnBw0HCXpBbqrq65DbhtjGPrgHV1ri9Jque4bjdAktQ5hrwkFcyQl6SCGfKSVDBDXpIKZshLUsEMeUkqmCEvSQUz5CWpYIa8JBXMkJekghnyklQwQ16SCmbIS1LBDHlJKpghL0kFM+QlqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwWqFfER8NiIejogHIuK2iJjbdOzaiNgREb+OiLfVb6okabLqjuQ3Aq/LzNcDjwDXAkTEOcBlwGuBC4H/iIhZNeuSJE1SrZDPzB9n5t5q925gUbW9Erg5M1/KzN8AO4BldeqSJE1eO+fkPwj8sNpeCDzZdGxnVXaEiBiKiK0RsXX37t1tbI4kafZ4J0TEncAZLQ6tzczbq3PWAnuB9aMva3F+trp+Zg4DwwADAwMtz5EkTc24IZ+ZFxzteESsBt4JrMjM0ZDeCSxuOm0R8NRUGylJmpq6q2suBK4GLs7MPU2HNgCXRcTxEXEWsBS4t05dkqTJG3ckP44bgOOBjREBcHdmXpGZ2yLiFuAhGtM4V2bmvpp1SZImqVbIZ+ZfHOXYOmBdnetLkurxE6+SVDBDXpIKZshLUsEMeUkqmCEvSQUz5CWpYIa8JBXMkJekghnyklQwQ16SCmbIS1LBDHlJKpghL0kFM+QlqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwQx5SSqYIS9JBTPkJalgtUI+Iv41Ih6IiPsj4scR8eqqPCLiixGxozr+pvY0V5I0GXVH8p/NzNdn5huA7wP/XJW/HVhafQ0BN9asR5I0BbVCPjP/2LT7Z0BW2yuBb2TD3cDciFhQpy5J0uTNrnuBiFgHrAKeB/6mKl4IPNl02s6qbFeL1w/RGO3T399ftzmSpCbjjuQj4s6I+FWLr5UAmbk2MxcD64GrRl/W4lLZoozMHM7MgcwcmD9//lT7IUlqYdyRfGZeMMFrfRP4AfAJGiP3xU3HFgFPTbp1kqRa6q6uWdq0ezHwcLW9AVhVrbI5D3g+M4+YqpEkdVbdOfnrIuIvgf3A48AVVfkdwDuAHcAe4AM165EkTUGtkM/MS8YoT+DKOteWJNXnJ14lqWCGvCQVzJCXpIIZ8pJUMENekgpmyEtSwQx5SSqYIS9JBTPkJalghrwkFcyQl6SCReMxM8eGiNhN40FnveY04HfdbkQXzMR+z8Q+w8zsdy/1+czMbPkHOY6pkO9VEbE1Mwe63Y7pNhP7PRP7DDOz36X02ekaSSqYIS9JBTPk22O42w3okpnY75nYZ5iZ/S6iz87JS1LBHMlLUsEMeUkqmCHfBhHx0YjIiDit2o+I+GJE7IiIByLiTd1uY7tExGcj4uGqX7dFxNymY9dWff51RLytm+3shIi4sOrbjoi4ptvt6YSIWBwRd0XE9ojYFhEfrspPjYiNEfFo9f2V3W5ru0XErIj4RUR8v9o/KyLuqfr8rYjo63Ybp8KQrykiFgNvAZ5oKn47sLT6GgJu7ELTOmUj8LrMfD3wCHAtQEScA1wGvBa4EPiPiJjVtVa2WdWXL9H42Z4D/H3V59LsBT6SmWcD5wFXVv28BtiUmUuBTdV+aT4MbG/a/wzwharPvwcu70qrajLk6/sC8DGg+Q72SuAb2XA3MDciFnSldW2WmT/OzL3V7t3Aomp7JXBzZr6Umb8BdgDLutHGDlkG7MjMxzJzBLiZRp+Lkpm7MvPn1fafaITeQhp9vak67SbgXd1pYWdExCLgb4GvVPsBnA98uzqlZ/tsyNcQERcDv83MXx52aCHwZNP+zqqsNB8Eflhtl97n0vt3hIhYArwRuAd4VWbugsYbAXB691rWEdfTGKztr/bnAX9oGtD07M97drcbcKyLiDuBM1ocWgt8HHhrq5e1KOuZtapH63Nm3l6ds5bGr/brR1/W4vye6fMElN6/Q0TEK4BbgTWZ+cfGwLZMEfFO4JnMvC8ilo8Wtzi1J3/ehvw4MvOCVuURcS5wFvDL6j/AIuDnEbGMxrv+4qbTFwFPdbipbTNWn0dFxGrgncCKPPhBi57u8wSU3r8DImIOjYBfn5nfqYqfjogFmbmrmnp8pnstbLs3AxdHxDuAE4CTaYzs50bE7Go037M/b6drpigzH8zM0zNzSWYuoRECb8rM/wU2AKuqVTbnAc+P/qrb6yLiQuBq4OLM3NN0aANwWUQcHxFn0bjpfG832tghPwOWVisu+mjcZN7Q5Ta1XTUX/VVge2Z+vunQBmB1tb0auH2629YpmXltZi6q/h9fBvwkM98L3AW8pzqtZ/vsSL4z7gDeQePm4x7gA91tTlvdABwPbKx+g7k7M6/IzG0RcQvwEI1pnCszc18X29lWmbk3Iq4CfgTMAr6Wmdu63KxOeDPwPuDBiLi/Kvs4cB1wS0RcTmMl2aVdat90uhq4OSI+BfyCxptfz/GxBpJUMKdrJKlghrwkFcyQl6SCGfKSVDBDXpIKZshLUsEMeUkq2P8DU6vLNXiQXVsAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "this_index=np.arange(Q['offset_start'], Q['offset_end'])\n",
    "plt.plot(x,y,'k.')\n",
    "plt.plot(10,0,'r*')\n",
    "plt.plot(x[this_index], y[this_index],'go')\n",
    "plt.axis('equal');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To avoid generating bin names by hand, we can just call the query_xy() method, which takes a tuple of two numpy arrays containing the bin locations.  This can be done for multiple bins, and the results will be stitched together into a useful set of query results.\n",
    "## The Geoindex class for files on disk\n",
    "The class is much more useful when we have a number of datasets on disk and we need to index them as a group.  Let's make a some data files on disk, which will be a set of diagonal parallel lines of points:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 218,
   "metadata": {},
   "outputs": [],
   "source": [
    "test_dir='test_data/for_geoindex'\n",
    "if not os.path.isdir(test_dir):\n",
    "    os.mkdir(test_dir)\n",
    "for offset in np.arange(-40, 50, 10):\n",
    "    out_file=test_dir+'/data_%d.h5' % offset\n",
    "    pc.data().from_dict({'x':x,'y':y+offset, 't':t*offset}).to_h5(out_file)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's make a geoIndex for the files and look at it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 219,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(-55.0, 55.0, -55.0, 55.0)"
      ]
     },
     "execution_count": 219,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "test_files=glob.glob(test_dir+'/*.h5')\n",
    "gi_2=pc.geoIndex(delta=[10,10]).for_files(test_files,'h5')\n",
    "xy_bin=gi_2.bins_as_array()\n",
    "plt.figure(); \n",
    "plt.plot(xy_bin[0], xy_bin[1],'r*')\n",
    "plt.axis('equal')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Looking at the entry for a particular bin shows how we store the index information:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 220,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'file_num': array([4, 5]), 'offset_start': array([65, 75]), 'offset_end': array([75, 75])}\n",
      "test_data/for_geoindex/data_-20.h5\n",
      "test_data/for_geoindex/data_-30.h5\n"
     ]
    }
   ],
   "source": [
    "print(gi_2['20_-20'])\n",
    "print(gi_2.attrs['file_4'])\n",
    "print(gi_2.attrs['file_5'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The contents of gi_2 at (20, -20) indicate that the data are in file number 4 for indices between 65 and 75, and in file 5, for indices between 75 and 75 (inclusive).  files 4 and 5 are test_data/for_geoindex/data_-20.h5\n",
    "test_data/for_geoindex/data_-30.h5, respectively.\n",
    "\n",
    "Let's retrieve the data for three bins:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[<class 'pointCollection.data.data'> with shape (20,),\n",
      "with fields:\n",
      "['x', 'y'], <class 'pointCollection.data.data'> with shape (19,),\n",
      "with fields:\n",
      "['x', 'y']]\n"
     ]
    }
   ],
   "source": [
    "D=gi_2.query_xy((np.array([10,20, 30, 40]), np.array([20, 20, 20, 20])), fields={None:['x','y']})\n",
    "print(D)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The result is a list of two pc.data objects, that together contain the data we requested:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXkAAAD4CAYAAAAJmJb0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAUrElEQVR4nO3dfZBddX3H8fc3WROgFoMEJSUpIVPsFG2rEGmoUilQQaXYzqjDSKdY6zAy6ogPoyCd0cI49Wl8murYjNTRio/4AFodn6pVZprgBuXBYjACgUCAhUZtBxVivv3jnMAl3N3N3nt3729/5/2aubP3nnv3e78cMp8997dnzzcyE0lSnZaMuwFJ0vwx5CWpYoa8JFXMkJekihnyklSxiXE30GvlypW5du3acbchSYvKli1b7s3Mw/o9V1TIr127lsnJyXG3IUmLSkRsn+45l2skqWKGvCRVzJCXpIoZ8pJUMUNekipmyEt6pJ074VnPgrvuKq/eqHvrAENe0iNdcglcdRVcfHF59UbdWwdESZcaXr9+fXqevDQmBx4Iv/rVo7cfcAD88pfjrTfq3ioTEVsyc32/5zySl9S4+WZ48YvhoIOaxwcdBGefDbfcMv56o+6tQwx5SY1Vq+Dgg5sj5gMOaL4efDAcfvj46426tw4x5CU97O674eUvh02bmq/D/oJzlPVG3VtHuCYvSYuca/KS1FGGvCRVzJCXpIoZ8pJUMUNekipmyEtSxQx5SaqYIS9JFTPkJalihrwkVcyQl6SKGfKSVDFDXpIqNrKQj4ilEfGDiPhy+/ioiNgcET+JiE9HxLJRvZcqVPJc0VHXK7m30us543XORnkk/2rgxp7Hbwfek5lHA7uAvx/he6k2Jc8VHXW9knsrvZ4zXudsJNeTj4jVwEeBtwKvBf4SmAIOz8zdEXEC8JbMPG2mOl5PvoNKnis66nol91Z6PWe8zmghrif/XuANwJ728aHAzzJzd/t4B3DENM2dGxGTETE5NTU1ona0aJQ8V3TU9UrurfR6zngd2NAhHxFnAPdk5pbezX1e2vcjQ2ZuzMz1mbn+sMMOG7YdLTYlzxUddb2Seyu9njNeBzaKI/lnAGdGxK3Ap4CTaY7sV0TERPua1cCdI3gv1ajkuaKjrldyb6XXc8brQEY64zUiTgJen5lnRMRngc9l5qci4kPAdZn5wZm+3zV5SZq7cc14fSPw2ojYRrNGf+k8vpckqY+J2V+y/zLzO8B32vs3A8ePsr4kaW78i1dJqpghL0kVM+QlqWKGvCRVzJCXpIoZ8pJUMUNekipmyEtSxQx5SaqYIS9JFTPkJalihnzJujRrs0v1Su6t9HrOeJ27zCzmdtxxx6V6nHde5pIlzdfS6pXcW+n1Su6t9Hqj7q0SwGROk6sjvZ78sLyefKtLsza7VK/k3kqv54zXGY3revIaVJdmbXapXsm9lV7PGa8DM+RL1KVZm12qV3JvpddzxuvADPlSdWnWZpfqldxb6fWc8ToQ1+QlaZFzTV6SOsqQl6SKGfKSVDFDXpIqNjHuBiTNk9uvhlu/BwceCr+8D9aeCGuOH3dXWmCGvFSL3lC/64fwg0/Abx4E9kAsgaXL4ZwrDfqOMeSlxWbfI/R+oU4APadH5x74zQPN9xnynWLIS6Wb6Qj9oTDfJ9TZ5+9fYgksXdYs2ahTDHmpFIMcoT90v0+oL5mAp/0NHP7Hrsl3mCEvjcsojtD3Pm+oaxqGvDTf5vsI3bNnNANDXho1j9BVkKFDPiLWAB8DDqf5V7wxM98XEY8HPg2sBW4FXpSZu4Z9P6lot18NHz0Tdv8aj9BVglH8xetu4HWZ+QfABuAVEXEMcAHwrcw8GvhW+1hz0aVZm7XUu/V7zamK7Gk39DtCbzcvWQbrXwpnvA9O/gd4yb/DGe+B9S+BE1/38NfZAr6WfbfQtbpiurmAg96AK4C/ALYCq9ptq4Cts32vM1730aVZm7XUu21z5iVPzHzzisw3H5z5lhWZF6/M/NL5md//SOZ335X5mlMzT1ye+aoXLGxvNdRzxmtfLNSM14hYC3wXeApwW2au6HluV2YeMtP3ez35VpdmbdZYb7rLCZTQ22Kt54zXGS3I9eQj4rHA54DzM/MXc/i+cyNiMiImp6amRtXO4talWZs11ltzfP/llhJ6K6jelu27+MC3t/GJzbfxgW9vY8v2GX5l54zXgY3k7JqIeAxNwF+WmZ9vN98dEasyc2dErALu6fe9mbkR2AjNkfwo+ln0ujRrs0v1Su5tHuttefyRbDr2qRzyf7vYtfJpHLL9AW74r+u5fMsOHty9p/n1RMCyiSVc9rINHHdknw/8zngd2CjOrgngUuDGzHx3z1NXAucAb2u/XjHse3XK3nmW554LGzc2v3AqpV7JvZVer+TeRlRvy/ZdbLr5Pg45aBk37FnH5S9+Dg/G0mZ9mCS/cP2jzjnak/Dg7j1suvm+/iE/ot66aOg1+Yh4JvA94HoePqXgTcBm4DPA7wK3AS/MzP+ZqZZr8tLi0Rvmu+5/oAn1O3/+iCP0fcN8OrMeyWtGM63JD30kn5lX8dB5YY9yyrD1JZXhEUfo04T5fv6JF0sCJpYEL1y/hif/zuPYdf8DbFh3qAE/D/yLV0mPMMgR+jR/4tU3zPfWNdQXhiEvdZxH6HUz5KWO8Ai9mwx5qQO2bN/F2R/exK8f9Ai9awx5qQM23XwfD7RH6+ARepcY8lIHbFh3KMsmlvDAg3secW1Mj9DrZ8hLHXDckYdw2cs2PGpN3lCvnyEvdcRxRx5imHfQyC5QJkkqjyEvSRUz5CWpYoZ8ybo0hq1L9UrurfR6jv+bu+lGRo3j5vi/fXRpDFuX6pXcW+n1HP/XFws1/m9YXmq41aUxbF2qV3Jvpddz/N+MFmT8n0ao5LFuJfdWer2Seyu9nuP/BmbIl6jksW4l91Z6vZJ7K72e4/8GZsiXau+os02bmq/D/qJplPVK7q30eiX3Vnq9UffWEa7JS9Ii55q8JHWUIS9JFTPkJalihrwkVcyQl6SKGfKSVDFDXpIqZshLUsUMeUmqmCEvSRUz5CWpYoa8JFXMkJekis17yEfE6RGxNSK2RcQF8/1+VenSrM0u1Su5t9LrOeN17qabCziKG7AU+CmwDlgGXAscM93rnfG6jy7N2uxSvZJ7K72eM177YlwzXiPiBOAtmXla+/jC9gfLP/V7vdeTb3Vp1maX6pXcW+n1nPE6o3FeT/4I4PaexzvabQ+JiHMjYjIiJqempua5nUWiS7M2u1Sv5N5Kr+eM14HNd8hHn22P+OiQmRszc31mrj/ssMPmuZ1FokuzNrtUr+TeSq/njNeBzXfI7wDW9DxeDdw5z+9Zhy7N2uxSvZJ7K72eM14HMt9r8hPATcApwB3A94EXZ+aP+r3eNXlJmruZ1uQn5vONM3N3RLwS+BrNmTb/Ol3AS5JGb15DHiAzvwJ8Zb7fR5L0aP7FqyRVzJCXpIoZ8pJUMUNekipmyEtSxQx5SaqYIS9JFTPkJalihrwkVcyQl6SKGfKSVDFDvmRdmrXZpXol91Z6PWe8zt10cwHHcXPG6z66NGuzS/VK7q30es547YtxzXidK68n3+rSrM0u1Su5t9LrOeN1RuOc8apBdGnWZpfqldxb6fWc8TowQ75EXZq12aV6JfdWej1nvA7MkC9Vl2Ztdqleyb2VXs8ZrwNxTV6SFjnX5CWpowx5SaqYIS9JFTPkJalihrwkVcyQl6SKGfKSVDFDXpIqZshLUsUMeUmqmCEvSRUz5CWpYkOFfES8MyJ+HBHXRcQXImJFz3MXRsS2iNgaEacN36okaa6GPZL/BvCUzPwj4CbgQoCIOAY4C3gycDrwwYhYOuR7dU+XZm12qV7JvZVezxmvczfdXMC53oC/Bi5r718IXNjz3NeAE2ar4YzXfXRp1maX6pXcW+n1nPHaFwsx4zUivgR8OjM/HhH/DGzKzI+3z10KfDUzL5+phteTb3Vp1maX6pXcW+n1nPE6o6GuJx8R34yIG/rcnt/zmouA3cBlezf1KdX3p0lEnBsRkxExOTU1Nft/TRd0adZml+qV3Fvp9ZzxOrCJ2V6QmafO9HxEnAOcAZySD38s2AGs6XnZauDOaepvBDZCcyS/Hz3Xr0uzNrtUr+TeSq/njNeBDXt2zenAG4EzM/P+nqeuBM6KiOURcRRwNHD1MO/VOV2atdmleiX3Vno9Z7wOZKg1+YjYBiwH7ms3bcrMl7fPXQS8lGYZ5/zM/Ops9VyTl6S5m2lNftblmplk5u/N8NxbgbcOU1+SNBz/4lWSKmbIS1LFDHlJqpghL0kVM+QlqWKGvCRVzJCXpIoZ8pJUMUNekipmyEtSxQx5SaqYIV+yLo1h61K9knsrvZ7j/+ZuupFR47g5/m8fXRrD1qV6JfdWej3H//XFQoz/GwUvNdzq0hi2LtUrubfS6zn+b0ZDjf/TGHRpDFuX6pXcW+n1HP83MEO+RF0aw9aleiX3Vno9x/8NzJAvVZfGsHWpXsm9lV7P8X8DcU1ekhY51+QlqaMMeUmqmCEvSRUz5CWpYoa8JFXMkJekihnyklQxQ16SKmbIS1LFDHlJqpghL0kVM+QlqWKGvCRVbCQhHxGvj4iMiJXt44iI90fEtoi4LiKOHcX7dE6XZm12qV7Jvak+080F3N8bsAb4GrAdWNluey7wVSCADcDm/anljNd9dGnWZpfqldybFiXmc8ZrRFwOXAJcAazPzHsj4l+A72TmJ9vXbAVOysydM9XyevKtLs3a7FK9knvTojZv15OPiDOBOzLz2n2eOgK4vefxjnZbvxrnRsRkRExOTU0N0049ujRrs0v1Su5N1ZqY7QUR8U2g3yDFi4A3Ac/u9219tvX9yJCZG4GN0BzJz9ZPJ3Rp1maX6pXcm6o165F8Zp6amU/Z9wbcDBwFXBsRtwKrgWsi4nCaI/c1PWVWA3eOvv2KdWnWZpfqldybqjSyGa9t0O9dk38e8EqaX8D+CfD+zDx+thquyUvS3M20Jj/rcs2AvkIT8NuA+4G/m6f3kSTNYGQhn5lre+4n8IpR1ZYkDca/eJWkihnyklQxQ16SKmbIS1LFDHlJqpghL0kVM+QlqWKGvCRVzJCXpIoZ8pJUMUNekipmyJes5FmgzhWVFgVDvmSXXAJXXQUXX1xevVH3JmlejOx68qPg9eRbJc8Cda6oVJx5m/GqeVLyLFDnikqLiiFfopJngTpXVFpUDPlSlTwL1Lmi0qLhmrwkLXKuyUtSRxnyklQxQ16SKmbIS1LFDHlJqpghL0kVK+oUyoiYArbP8rKVwL0L0M6g7G9wJfcGZfdXcm9Qdn8l9wb719+RmXlYvyeKCvn9ERGT050PWgL7G1zJvUHZ/ZXcG5TdX8m9wfD9uVwjSRUz5CWpYosx5DeOu4FZ2N/gSu4Nyu6v5N6g7P5K7g2G7G/RrclLkvbfYjySlyTtJ0Nekiq2aEI+Ip4aEZsi4ocRMRkRx7fbIyLeHxHbIuK6iDh2jD2+KiK2RsSPIuIdPdsvbPvbGhGnjbG/10dERsTK9nER+y4i3hkRP257+EJErOh5buz7LiJOb99/W0RcMI4e9ulnTUR8OyJubP+tvbrd/viI+EZE/KT9esgYe1waET+IiC+3j4+KiM1tb5+OiGVj7G1FRFze/pu7MSJOKGXfRcRr2v+nN0TEJyPigKH3XWYuihvwdeA57f3nAt/puf9VIIANwOYx9ffnwDeB5e3jJ7RfjwGuBZYDRwE/BZaOob81wNdo/thsZWH77tnARHv/7cDbS9l3wNL2fdcBy9p+jhnHfurpaRVwbHv/t4Gb2n31DuCCdvsFe/fjmHp8LfAJ4Mvt488AZ7X3PwScN8bePgq8rL2/DFhRwr4DjgBuAQ7s2WcvGXbfLZojeSCBg9v7jwPubO8/H/hYNjYBKyJi1Rj6Ow94W2b+GiAz7+np71OZ+evMvAXYBhw/hv7eA7yBZj/uVcS+y8yvZ+bu9uEmYHVPf+Ped8cD2zLz5sx8APhU29fYZObOzLymvf+/wI00AfF8mgCj/fpX4+gvIlYDzwM+3D4O4GTg8gJ6Oxj4M+BSgMx8IDN/RiH7DpgADoyICeAgYCdD7rvFFPLnA++MiNuBdwEXttuPAG7ved2OdttCexJwYvux6j8j4unt9rH3FxFnAndk5rX7PDX23vp4Kc2nCyijvxJ6mFZErAWeBmwGnpiZO6H5QQA8YUxtvZfmgGJP+/hQ4Gc9P8jHuQ/XAVPAR9rlpA9HxG9RwL7LzDtosu02mnD/ObCFIffdxCibHFZEfBPoNxH6IuAU4DWZ+bmIeBHNT+JTaZYa9jUv54XO0t8EcAjNssfTgc9ExLqF6m+W3t5EsyTyqG/rs23B911mXtG+5iJgN3DZQvc3gxJ66CsiHgt8Djg/M3/RHDCPV0ScAdyTmVsi4qS9m/u8dFz7cAI4FnhVZm6OiPfRLM+MXft7gOfTLE3+DPgs8Jw+L53Tvisq5DPz1Omei4iPAa9uH36W9qMgzU+2NT0vXc3DSzkL2d95wOezWTi7OiL20FxYaEH6m663iPhDmn8017YhsBq4pv3FdRH7ru3zHOAM4JR2H7KQ/c2ghB4eJSIeQxPwl2Xm59vNd0fEqszc2S673TN9hXnzDODMiHgucADNEut7aZYCJ9oj0nHuwx3Ajszc3D6+nCbkS9h3pwK3ZOYUQER8HvhThtx3i2m55k7gWe39k4GftPevBP62PVNkA/DzvR+7FtgX276IiCfR/ELn3ra/syJieUQcBRwNXL1QTWXm9Zn5hMxcm5lraf6RH5uZd1HIvouI04E3Amdm5v09T41137W+DxzdnuGwDDir7Wts2jXuS4EbM/PdPU9dCZzT3j8HuGKhe8vMCzNzdftv7SzgPzLzbODbwAvG2Vvb313A7RHx++2mU4D/poB9R7NMsyEiDmr/H+/tbbh9t9C/QR7iN8/PpFmfupZm/fG4dnsAH6A5A+J6YP2Y+lsGfBy4AbgGOLnnuYva/rbSniE0xv14Kw+fXVPKvttGs+79w/b2oZL2Hc1ZSDe1fVw0zv9/bT/PpPnIfl3PPnsuzdr3t2gOgL4FPH7MfZ7Ew2fXrKP5Ab2N5pP48jH29VRgst1/X6RZZi1i3wH/CPy4zZF/ozmzbKh952UNJKlii2m5RpI0R4a8JFXMkJekihnyklQxQ16SKmbIS1LFDHlJqtj/A2uQi5fBZ7/GAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.plot(xy_bin[0], xy_bin[1],'r*')\n",
    "plt.axis('equal')\n",
    "for Di in D: \n",
    "    plt.plot(Di.x, Di.y,'.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can also query a range of bins using the query_xy_box() method.  Let's get all the data for bins between x=0 and x=30, and for bins between y=-20 and y=20."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 223,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'test_data/for_geoindex/data_0.h5': {'type': 'h5', 'offset_start': array([45]), 'offset_end': array([55]), 'x': array([0]), 'y': array([0])}}\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "XR=np.array([0, 30])\n",
    "YR=np.array([-20, 20])\n",
    "\n",
    "D=gi_2.query_xy_box(XR, YR, fields={None:['x','y']})\n",
    "plt.plot(xy_bin[0], xy_bin[1],'r*')\n",
    "plt.axis('equal')\n",
    "for Di in D: \n",
    "    plt.plot(Di.x, Di.y,'.')\n",
    "plt.plot(XR[[0, 0, 1, 1, 0]], YR[[0, 1, 1, 0, 0]],'k')\n",
    "\n",
    "D1=gi_2.query_xy((np.array(0), np.array(0)), fields={None:['x','y']}, get_data=False)\n",
    "print(D1)\n",
    "#plt.plot(D1[0].x, D1[0].y,'mo')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Note that the recovered data extend outside the box that we specified, because query_xy_box finds the data for the bin centers within the box, and each bin extends 1/2 of the bin spacing around its center."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Changing data paths\n",
    "Let's look again at how the files containing the data in gi_2 are specified:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 224,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "test_data/for_geoindex/data_40.h5\n"
     ]
    }
   ],
   "source": [
    "print(gi_2.attrs['file_0'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The files specified relative to the current directory, which means that if we use the geoindex from a different directory, it won't work.  The way to fix this is to specify a 'dir_root' attribute for the index during its creation.  The files will then be specified relative to that location."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 234,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "test_data/for_geoindex/data_40.h5\n",
      "/Users/ben/git_repos/pointCollection/\n"
     ]
    }
   ],
   "source": [
    "gi_3=pc.geoIndex(delta=[10,10]).for_files(test_files,'h5', dir_root=os.getcwd()+'/')\n",
    "print(gi_3.attrs['file_0'])\n",
    "print(gi_3.attrs['dir_root'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "It is then possible to change the root location of a geoIndex, which is handy when moving groups of data files:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 235,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "data_40.h5\n",
      "/Users/ben/git_repos/pointCollection/test_data/for_geoindex/\n"
     ]
    }
   ],
   "source": [
    "gi_3.change_root(os.getcwd()+'/'+test_dir+'/')\n",
    "print(gi_3.attrs['file_0'])\n",
    "print(gi_3.attrs['dir_root'])"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
