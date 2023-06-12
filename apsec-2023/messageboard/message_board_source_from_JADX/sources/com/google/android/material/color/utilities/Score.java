package com.google.android.material.color.utilities;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public final class Score {
    private static final double CUTOFF_CHROMA = 15.0d;
    private static final double CUTOFF_EXCITED_PROPORTION = 0.01d;
    private static final double CUTOFF_TONE = 10.0d;
    private static final double TARGET_CHROMA = 48.0d;
    private static final double WEIGHT_CHROMA_ABOVE = 0.3d;
    private static final double WEIGHT_CHROMA_BELOW = 0.1d;
    private static final double WEIGHT_PROPORTION = 0.7d;

    private Score() {
    }

    public static List<Integer> score(Map<Integer, Integer> map) {
        boolean z;
        double d = 0.0d;
        for (Map.Entry<Integer, Integer> value : map.entrySet()) {
            d += (double) ((Integer) value.getValue()).intValue();
        }
        HashMap hashMap = new HashMap();
        double[] dArr = new double[361];
        for (Map.Entry next : map.entrySet()) {
            int intValue = ((Integer) next.getKey()).intValue();
            Cam16 fromInt = Cam16.fromInt(intValue);
            hashMap.put(Integer.valueOf(intValue), fromInt);
            int round = (int) Math.round(fromInt.getHue());
            dArr[round] = dArr[round] + (((double) ((Integer) next.getValue()).intValue()) / d);
        }
        HashMap hashMap2 = new HashMap();
        for (Map.Entry entry : hashMap.entrySet()) {
            int intValue2 = ((Integer) entry.getKey()).intValue();
            int round2 = (int) Math.round(((Cam16) entry.getValue()).getHue());
            double d2 = 0.0d;
            for (int i = round2 - 15; i < round2 + 15; i++) {
                d2 += dArr[MathUtils.sanitizeDegreesInt(i)];
            }
            hashMap2.put(Integer.valueOf(intValue2), Double.valueOf(d2));
        }
        HashMap hashMap3 = new HashMap();
        for (Map.Entry entry2 : hashMap.entrySet()) {
            int intValue3 = ((Integer) entry2.getKey()).intValue();
            Cam16 cam16 = (Cam16) entry2.getValue();
            hashMap3.put(Integer.valueOf(intValue3), Double.valueOf((((Double) hashMap2.get(Integer.valueOf(intValue3))).doubleValue() * 100.0d * WEIGHT_PROPORTION) + ((cam16.getChroma() - TARGET_CHROMA) * (cam16.getChroma() < TARGET_CHROMA ? WEIGHT_CHROMA_BELOW : WEIGHT_CHROMA_ABOVE))));
        }
        List<Integer> filter = filter(hashMap2, hashMap);
        HashMap hashMap4 = new HashMap();
        for (Integer intValue4 : filter) {
            int intValue5 = intValue4.intValue();
            hashMap4.put(Integer.valueOf(intValue5), (Double) hashMap3.get(Integer.valueOf(intValue5)));
        }
        ArrayList<Map.Entry> arrayList = new ArrayList<>(hashMap4.entrySet());
        Collections.sort(arrayList, new ScoredComparator());
        ArrayList arrayList2 = new ArrayList();
        for (Map.Entry entry3 : arrayList) {
            Cam16 cam162 = (Cam16) hashMap.get(Integer.valueOf(((Integer) entry3.getKey()).intValue()));
            Iterator it = arrayList2.iterator();
            while (true) {
                if (it.hasNext()) {
                    if (MathUtils.differenceDegrees(cam162.getHue(), ((Cam16) hashMap.get((Integer) it.next())).getHue()) < CUTOFF_CHROMA) {
                        z = true;
                        break;
                    }
                } else {
                    z = false;
                    break;
                }
            }
            if (!z) {
                arrayList2.add((Integer) entry3.getKey());
            }
        }
        if (arrayList2.isEmpty()) {
            arrayList2.add(-12417548);
        }
        return arrayList2;
    }

    private static List<Integer> filter(Map<Integer, Double> map, Map<Integer, Cam16> map2) {
        ArrayList arrayList = new ArrayList();
        for (Map.Entry next : map2.entrySet()) {
            int intValue = ((Integer) next.getKey()).intValue();
            double doubleValue = map.get(Integer.valueOf(intValue)).doubleValue();
            if (((Cam16) next.getValue()).getChroma() >= CUTOFF_CHROMA && ColorUtils.lstarFromArgb(intValue) >= CUTOFF_TONE && doubleValue >= CUTOFF_EXCITED_PROPORTION) {
                arrayList.add(Integer.valueOf(intValue));
            }
        }
        return arrayList;
    }

    static class ScoredComparator implements Comparator<Map.Entry<Integer, Double>> {
        public int compare(Map.Entry<Integer, Double> entry, Map.Entry<Integer, Double> entry2) {
            return -entry.getValue().compareTo(entry2.getValue());
        }
    }
}
