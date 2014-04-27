# CrowdPace
# Running calculator: http://frommorningside.blogspot.com/2014/04/let-crowd-suggest-pace.html 
# Ivan Zalamea, 2014
#
# This script uses fits that rely on public race results from nyrr.org

import numpy as np

def findTime(percentage,mu,sigma):
    #finds time for given percentile for a log-normal with mu and sigma
    tl=0.1
    tu=1000
    tt=0.5*(tu+tl)
    per=slowerthan(tt,mu,sigma)

    while (per-percentage)*(per-percentage)>0.00000000001*percentage*percentage:
        if per>percentage:
            tu=tt
        else:
            tl=tt
        tt=0.5*(tu+tl)
        per=slowerthan(tt,mu,sigma)
    return tt

def slowerthan(time,mu,sigma):
    return 0.5*(1.+erf((np.log(time)-mu)/(sigma*np.sqrt(2.))))
    #return 0.5*(1.+scipy.special.erf((np.log(time)-mu)/(sigma*np.sqrt(2.))))

# erf(z) from: http://www.cs.princeton.edu/introcs/21function/ErrorFunction.java.html
# Implements the Gauss error function.
#   erf(z) = 2 / sqrt(pi) * integral(exp(-t*t), t = 0..z)
#
# fractional error in math formula less than 1.2 * 10 ^ -7.
# although subject to catastrophic cancellation when z in very close to 0
# from Chebyshev fitting formula for erf(z) from Numerical Recipes, 6.2
def erf(z):
	t = 1.0 / (1.0 + 0.5 * abs(z))
    	# use Horner's method
        ans = 1 - t * np.exp( -z*z -  1.26551223 +
        					t * ( 1.00002368 +
        					t * ( 0.37409196 + 
        					t * ( 0.09678418 + 
        					t * (-0.18628806 + 
        					t * ( 0.27886807 + 
        					t * (-1.13520398 + 
        					t * ( 1.48851587 + 
        					t * (-0.82215223 + 
        					t * ( 0.17087277))))))))))
        if z >= 0.0:
        	return ans
        else:
        	return -ans

    
def predictedPace(gender,knowntime,distance,newdistance):
    """ The following data comes from fitting log-normal distributions 
        to finishing times distributions for distances from 1 mile to 50 miles.
        the columns are distance, mu for men, sigma for men, mu for women, sigma for women.
        (mu and sigma are the standard mu and sigma for a log-normal)
     """
    data=[[1,1.82479886,0.15442097,2.02078846,0.152018],\
          [2,2.81269131,0.24298622,2.94027249,0.19785733],\
          [3.1,3.21439758,0.20199374,3.38934256,0.17998415],\
          [4,3.48733053,0.17403963,3.63338083,0.15416951],\
          [5,3.69988339,0.1828273,3.85497481,0.15342633],\
          [6.2,3.92248345,0.17043469,4.08229446,0.15731007],\
          [7,4.03585866,0.15658534,4.15885728,0.12602283],\
          [8,4.1804725,0.13912475,4.29095087,0.11099218],\
          [9.3,4.34819542,0.16160759,4.47210575,0.13358565],\
          [10,4.39081844,0.16460379,4.52142994,0.13755774],\
          [13.1,4.71140604,0.16332366,4.84067277,0.14722737],\
          [18,5.08558166,0.15552566,5.19199923,0.13465799],\
          [20,5.07063126,0.15512254,5.18039573,0.12522386],\
          [26.2,5.50908488,0.18280742,5.62205952,0.16401895],\
          [37.28,5.9248495,0.17540027,6.01767465,0.15617823],\
          [50,6.18750376,0.13950345,6.23711374,0.11798467]]

    datalog=[[0.0,1.82479886,0.15442097,2.02078846,0.152018],\
          [0.69314718056,2.81269131,0.24298622,2.94027249,0.19785733],\
          [1.13140211149,3.21439758,0.20199374,3.38934256,0.17998415],\
          [1.38629436112,3.48733053,0.17403963,3.63338083,0.15416951],\
          [1.60943791243,3.69988339,0.1828273,3.85497481,0.15342633],\
          [1.82454929205,3.92248345,0.17043469,4.08229446,0.15731007],\
          [1.94591014906,4.03585866,0.15658534,4.15885728,0.12602283],\
          [2.07944154168,4.1804725,0.13912475,4.29095087,0.11099218],\
          [2.23001440016,4.34819542,0.16160759,4.47210575,0.13358565],\
          [2.30258509299,4.39081844,0.16460379,4.52142994,0.13755774],\
          [2.57261223021,4.71140604,0.16332366,4.84067277,0.14722737],\
          [2.8903717579,5.08558166,0.15552566,5.19199923,0.13465799],\
          [2.99573227355,5.07063126,0.15512254,5.18039573,0.12522386],\
          [3.26575941077,5.50908488,0.18280742,5.62205952,0.16401895],\
          [3.61845698982,5.9248495,0.17540027,6.01767465,0.15617823],\
          [3.91202300543,6.18750376,0.13950345,6.23711374,0.11798467]]

    gender=gender.lower()
    distance=np.log(distance)
    
    imu=1
    isigma=2
    if gender=='f':
        imu=3
        isigma=4

    knownmu=my_interpol(datalog,imu,distance)
    knownsigma=my_interpol(datalog,isigma,distance)
        
    knownpercentage=slowerthan(knowntime,knownmu,knownsigma)

    newdistance=np.log(newdistance)
    newmu=my_interpol(datalog,imu,newdistance)
    newsigma=my_interpol(datalog,isigma,newdistance)
    return findTime(knownpercentage,newmu,newsigma)

def my_interpol(data,col,distance):
    if distance<=0.0:
        return data[0][col]
    if distance>=3.91202300543:
        return data[len(data)-1][col]
    i=0
    while data[i][0]<=distance:
        i=i+1

    return data[i-1][col]+(distance-data[i-1][0])*(data[i][col]-data[i-1][col])/(data[i][0]-data[i-1][0])

    
def main():    
    gender=raw_input('Predict time for male or female (M/F)? ')
    dist1=input('Enter distance in miles for base race: ')
    time=input('Enter time in minutes for base race: ')
    dist2=input('Enter distance in miles for which to predict finishing time: ')
    pt=predictedPace(gender,time,dist1,dist2)
    print "Estimated finishing time for "+str(dist2)+' miles:'
    print str(int(pt/60))+':'+str(int(pt%60))+':'+str(int((pt%60-int(pt%60))*60))
    print 
    print 'This is a pace of:'
    print str(int(pt/dist2%60))+':'+str(int((pt/dist2%60-int(pt/dist2%60))*60))+' minutes per mile'

    return

if __name__ == '__main__':
    main()
